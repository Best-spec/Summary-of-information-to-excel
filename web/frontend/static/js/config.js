// กำหนด ID ของ HTML elements ที่คุณต้องการอ้างถึง
export const ELEMENT_IDS = {
    welcome: 'mainContent',
    dropZone: 'dropZone',
    fileInput: 'fileInput',
    fileItems: 'fileItems',
    fileCount: 'fileCount',
    emptyState: 'emptyState',
    analysisButton: 'analysisButton',
    analysisResults: 'analysisResults',
    AnalysisActions: 'Analysis_Actions',
    contentAnalysis: 'contentAnalysis',
};

// ฟังก์ชันสำหรับดึง DOM element โดยใช้ ID จาก ELEMENT_IDS
export function getDomElements() {
    const elements = {};
    for (const key in ELEMENT_IDS) {
        if (ELEMENT_IDS.hasOwnProperty(key)) {
            elements[key] = document.getElementById(ELEMENT_IDS[key]);
        }
    }
    return elements;
}