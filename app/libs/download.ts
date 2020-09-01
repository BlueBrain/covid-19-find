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

export const readSingleFile = (e: Event): Promise<string | ArrayBuffer> => {
  return new Promise((resolve, reject) => {
    const file = (e.target as HTMLInputElement).files[0];
    if (!file) {
      resolve(null);
    }
    const reader = new FileReader();
    reader.onload = e => {
      const contents = e.target.result;
      resolve(contents);
    };
    reader.onerror = reject;
    reader.readAsText(file);
  });
};
