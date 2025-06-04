import { loadSummary } from "./api.js";
import { getDomElements } from "./config.js";
import { renderCharts } from "./graph.js";
import { showDataCards } from "./events.js";

let DOM = {}; // สร้างตัวแปร global (ภายใน script.js) สำหรับเก็บ DOM elements

document.addEventListener('DOMContentLoaded', function() {
    // ดึง DOM elements ทั้งหมดมาเก็บไว้ในตัวแปร DOM
    DOM = getDomElements();

    let uploadedFiles = [];
    let fileIdCounter = 0;

    // Drag and drop functionality
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropZone.classList.add('drag-active');
    }

    function unhighlight() {
        dropZone.classList.remove('drag-active');
    }

    dropZone.addEventListener('drop', handleDrop, false);
    fileInput.addEventListener('change', handleFileSelect, false);

    function handleDrop(e) {
        const files = e.dataTransfer.files;
        handleFiles(files);
    }

    function handleFileSelect(e) {
        const files = e.target.files;
        handleFiles(files);
    }

    function handleFiles(files) {
        Array.from(files).forEach(file => {
            const fileObj = {
                id: ++fileIdCounter,
                name: file.name,
                size: file.size,
                type: file.type,
                lastModified: file.lastModified
            };
            uploadedFiles.push(fileObj);
        });
        updateFileList();
    }

    function removeFile(id) {
        uploadedFiles = uploadedFiles.filter(file => file.id !== id);
        updateFileList();
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    function getFileIcon(type) {
        if (type.startsWith('image/')) return '🖼️';
        if (type.startsWith('video/')) return '🎥';
        if (type.startsWith('audio/')) return '🎵';
        if (type.includes('pdf')) return '📄';
        if (type.includes('text')) return '📝';
        if (type.includes('zip') || type.includes('rar')) return '🗜️';
        if (type.includes('word')) return '📘';
        if (type.includes('excel')) return '📊';
        if (type.includes('powerpoint')) return '📊';
        return '📁';
    }

    function updateFileList() {
        fileCount.textContent = uploadedFiles.length;
        
        if (uploadedFiles.length === 0) {
            emptyState.style.display = 'block';
            fileItems.innerHTML = '';
        } else {
            emptyState.style.display = 'none';
            fileItems.innerHTML = uploadedFiles.map(file => 
                '<div class="file-item">' +
                    '<div class="file-icon">' + getFileIcon(file.type) + '</div>' +
                    '<div class="file-info">' +
                        '<div class="file-name">' + file.name + '</div>' +
                        '<div class="file-size">' + formatFileSize(file.size) + '</div>' +
                    '</div>' +
                    '<button class="remove-btn" onclick="removeFile(' + file.id + ')">❌</button>' +
                '</div>'
            ).join('');
        }
    }

    function contentAnalysis() {
        const button = document.getElementById('analysisButton');
        if (button) {
        button.addEventListener('click', async () => { // ใส่ async ตรงนี้
            console.log('okkk');
            const text = document.getElementById('textresult');
            const analysisResults = document.getElementById('analysisResults');
            DOM.welcome.classList.add('hidden')
            DOM.contentAnalysis.classList.remove('hidden')
            await loadSummary();
        });
        }
    }

    function show() {
        console.log("Welcome div element:", DOM.welcome);
    }

    showDataCards();
    renderCharts();
    contentAnalysis();
    updateFileList();
});

  
// Initialize
// updateFileList();
// show();


