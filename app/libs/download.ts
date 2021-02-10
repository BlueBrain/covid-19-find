import { jsPDF } from 'jspdf';
import domToImage from 'dom-to-image';

export const download = (filename: string, mediaType: string, data: any) => {
  const blob = new Blob([data], { type: mediaType });
  if (window.navigator.msSaveBlob) {
    window.navigator.msSaveBlob(blob, filename);
  } else {
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
  }
};

export const readSingleFile = (
  e: Event,
): Promise<{ name: string; contents: string | ArrayBuffer }> => {
  return new Promise((resolve, reject) => {
    const file = (e.target as HTMLInputElement).files[0];
    if (!file) {
      resolve(null);
    }
    const reader = new FileReader();
    reader.onload = e => {
      const contents = e.target.result;
      resolve({ name: file.name, contents });
    };
    reader.onerror = reject;
    reader.readAsText(file);
  });
};

export const PDFFromElement = (element: HTMLElement) => {
  const { offsetWidth: w, offsetHeight: h } = element;
  const doc = new jsPDF('p', 'px', [w, h]);
  if (doc) {
    domToImage
      .toPng(element, { style: { 'background-color': 'white' } })
      .then(imgData => {
        doc.addImage(imgData, 'PNG', 0, 0, w, h);
        doc.save('scenario.pdf');
      });
  }
};
