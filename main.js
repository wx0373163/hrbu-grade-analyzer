const { app, BrowserWindow, shell, session, dialog } = require('electron');
const path = require('path');
const fs = require('fs');

function createWindow() {
  const win = new BrowserWindow({
    width: 1440,
    height: 900,
    minWidth: 1024,
    minHeight: 700,
    backgroundColor: '#1a1d23',
    autoHideMenuBar: true,
    show: true,
    icon: path.join(__dirname, 'build', 'icon.png'),
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      webSecurity: true,
      // Renderer runs as a normal web page: localStorage, FileReader,
      // Blob downloads all behave exactly like in a browser.
    },
  });

  win.loadFile(path.join(__dirname, 'src', 'index.html'));
  win.setTitle('哈尔滨学院成绩分析工作平台 v2.01');

  // Open links that would navigate to the real web in the user's browser,
  // keep everything else inside the app.
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith('http:') || url.startsWith('https:')) {
      shell.openExternal(url);
    }
    return { action: 'deny' };
  });

  win.webContents.on('will-navigate', (event, url) => {
    if (url.startsWith('http:') || url.startsWith('https:')) {
      event.preventDefault();
      shell.openExternal(url);
    }
  });
}

// Show a native "Save As" dialog for every export (CSV / XLSX / JSON / PNG),
// so the user picks where to save — exactly like a browser does when you
// click an export link. The dialog itself handles overwrite confirmation.
// Cancelling the dialog aborts the download.
app.whenReady().then(() => {
  const FILTERS = {
    '.csv': [{ name: 'CSV 文件', extensions: ['csv'] }],
    '.xlsx': [{ name: 'Excel 工作簿', extensions: ['xlsx'] }],
    '.json': [{ name: 'JSON 文件', extensions: ['json'] }],
    '.png': [{ name: 'PNG 图片', extensions: ['png'] }],
  };

  session.defaultSession.on('will-download', (event, item) => {
    let filename = item.getFilename();
    if (!filename || filename === 'download') {
      filename = '成绩分析导出_' + Date.now();
    }
    const ext = path.extname(filename).toLowerCase();
    const specific = FILTERS[ext] || [];
    const filters = [...specific, { name: '所有文件', extensions: ['*'] }];

    const defaultPath = path.join(app.getPath('downloads'), filename);
    const result = dialog.showSaveDialogSync({
      title: '选择保存位置',
      defaultPath,
      filters,
    });

    if (!result) {
      event.preventDefault();
      item.cancel();
      return;
    }
    item.setSavePath(result);
  });

  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
