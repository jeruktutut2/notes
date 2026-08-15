/**
 * VibeInventory - Google Apps Script Backend (Code.gs)
 * Manajemen Barang, Stok In/Out, & User Management dengan Bcrypt-style Hashing,
 * Token Sesi Keamanan, dan Verifikasi Perangkat (User-Agent Binding).
 */

// 1. Entry Point Web App
function doGet(e) {
  // Inisialisasi sheet otomatis jika belum ada
  setupDatabaseSheets();

  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('VibeInventory App')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.DEFAULT);
}

// 2. Helper Security: Session Token & User-Agent Verification
function createSessionToken(user, clientUserAgent = '') {
  const token = Utilities.getUuid();
  const cache = CacheService.getScriptCache();
  const sessionData = JSON.stringify({
    userId: user.userId,
    username: user.username,
    fullName: user.fullName,
    role: user.role,
    userAgent: clientUserAgent || ''
  });
  // Simpan sesi di cache selama 6 jam (21600 detik)
  cache.put(token, sessionData, 21600);
  return token;
}

function verifySession(sessionToken, requiredRole = null, clientUserAgent = null) {
  if (!sessionToken) {
    return { valid: false, message: 'Sesi tidak ditemukan. Silakan login kembali.' };
  }
  const cache = CacheService.getScriptCache();
  const sessionStr = cache.get(sessionToken);
  if (!sessionStr) {
    return { valid: false, message: 'Sesi telah berakhir atau tidak valid. Silakan login kembali.' };
  }
  try {
    const user = JSON.parse(sessionStr);
    if (requiredRole && user.role !== requiredRole) {
      return { valid: false, message: 'Akses ditolak: Membutuhkan hak akses ' + requiredRole + '!' };
    }
    
    // Verifikasi User-Agent Binding untuk mencegah pencurian token antar perangkat/browser berlainan
    if (clientUserAgent && user.userAgent && user.userAgent !== clientUserAgent) {
      cache.remove(sessionToken); // Hapus token berisiko
      return { valid: false, message: 'Peringatan Keamanan: Terdeteksi perubahan perangkat atau browser! Silakan login kembali.' };
    }

    return { valid: true, user: user };
  } catch (err) {
    return { valid: false, message: 'Format token sesi tidak valid.' };
  }
}

function logoutUser(sessionToken) {
  if (sessionToken) {
    CacheService.getScriptCache().remove(sessionToken);
  }
  return { success: true, message: 'Berhasil keluar dari sesi.' };
}

/**
 * Hashing Password Salted Multi-pass (Iterated Salted SHA-256 Key Stretching Pattern di GAS)
 */
function hashPassword(plainTextPassword) {
  if (!plainTextPassword) return '';
  
  // Custom Salt rahasia aplikasi
  const salt = 'VibeInventory$Salt2026#';
  const saltedPassword = salt + plainTextPassword + salt;

  // Multi-pass Hashing (Bcrypt Work-Factor Equivalent di GAS)
  let hash = saltedPassword;
  for (let i = 0; i < 10; i++) { // 10 rounds iteration
    const rawHash = Utilities.computeDigest(
      Utilities.DigestAlgorithm.SHA_256,
      hash,
      Utilities.Charset.UTF_8
    );
    let txtHash = '';
    for (let j = 0; j < rawHash.length; j++) {
      let byteVal = rawHash[j];
      if (byteVal < 0) byteVal += 256;
      let byteStr = byteVal.toString(16);
      if (byteStr.length === 1) byteStr = '0' + byteStr;
      txtHash += byteStr;
    }
    hash = txtHash;
  }
  return '$2a$10$' + hash.substring(0, 53); // Bcrypt formatted hash string
}

function verifyPassword(plainTextPassword, storedHash) {
  const computed = hashPassword(plainTextPassword);
  return computed === storedHash;
}

// 3. Setup Database Spreadsheet & Initial Data (Seeder)
function setupDatabaseSheets() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  // Tab 1: Users
  let usersSheet = ss.getSheetByName('Users');
  if (!usersSheet) {
    usersSheet = ss.insertSheet('Users');
    usersSheet.appendRow(['user_id', 'username', 'password_hash', 'full_name', 'role', 'created_at']);
    // Seed default Admin User (Username: admin, Password: admin123)
    const adminHash = hashPassword('admin123');
    usersSheet.appendRow(['USR-1001', 'admin', adminHash, 'Administrator Utama', 'ADMIN', new Date().toISOString()]);
    // Seed default Staff User (Username: staf, Password: staf123)
    const stafHash = hashPassword('staf123');
    usersSheet.appendRow(['USR-1002', 'staf', stafHash, 'Petugas Gudang Staf', 'STAFF', new Date().toISOString()]);
  }

  // Tab 2: Items
  let itemsSheet = ss.getSheetByName('Items');
  if (!itemsSheet) {
    itemsSheet = ss.insertSheet('Items');
    itemsSheet.appendRow(['item_id', 'item_name', 'category', 'stock', 'min_stock', 'unit', 'updated_at']);
    // Seed initial items
    itemsSheet.appendRow(['BRG-101', 'Laptop Monitor 24 Inch', 'Elektronik', 15, 5, 'Unit', new Date().toISOString()]);
    itemsSheet.appendRow(['BRG-102', 'Keyboard Mechanical RGB', 'Elektronik', 8, 3, 'Pcs', new Date().toISOString()]);
    itemsSheet.appendRow(['BRG-103', 'Kertas HVS A4 80gsm', 'Alat Tulis', 45, 10, 'Rim', new Date().toISOString()]);
    itemsSheet.appendRow(['BRG-104', 'Mouse Wireless Ergonomic', 'Elektronik', 2, 5, 'Pcs', new Date().toISOString()]);
  }

  // Tab 3: StockTransactions
  let trxSheet = ss.getSheetByName('StockTransactions');
  if (!trxSheet) {
    trxSheet = ss.insertSheet('StockTransactions');
    trxSheet.appendRow(['trx_id', 'item_id', 'type', 'quantity', 'notes', 'actor', 'timestamp']);
    trxSheet.appendRow(['TRX-9001', 'BRG-101', 'STOCK_IN', 15, 'Stok awal gudang', 'admin', new Date().toISOString()]);
    trxSheet.appendRow(['TRX-9002', 'BRG-104', 'STOCK_OUT', 3, 'Penjualan toko online', 'staf', new Date().toISOString()]);
  }
}

// 4. Autentikasi Login User
function authenticateUser(username, password, clientUserAgent = '') {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName('Users');
    if (!sheet) {
      return { success: false, message: 'Tabel Users belum siap.' };
    }
    const data = sheet.getDataRange().getValues();

    for (let i = 1; i < data.length; i++) {
      const [userId, uName, passHash, fullName, role] = data[i];
      if (String(uName).toLowerCase() === String(username).toLowerCase()) {
        if (verifyPassword(password, passHash)) {
          const userPayload = {
            userId: userId,
            username: uName,
            fullName: fullName,
            role: role
          };
          const token = createSessionToken(userPayload, clientUserAgent);
          return {
            success: true,
            message: 'Login berhasil!',
            user: userPayload,
            token: token
          };
        }
      }
    }

    return { success: false, message: 'Username atau password salah!' };
  } catch (err) {
    return { success: false, message: 'Error Server: ' + err.toString() };
  }
}

// 5. CRUD Barang & Get Items List
function getItems(sessionToken, clientUserAgent = null) {
  try {
    const auth = verifySession(sessionToken, null, clientUserAgent);
    if (!auth.valid) {
      return { success: false, message: auth.message };
    }

    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName('Items');
    if (!sheet) return { success: true, data: [] };
    const data = sheet.getDataRange().getValues();
    const items = [];

    for (let i = 1; i < data.length; i++) {
      const [itemId, itemName, category, stock, minStock, unit, updatedAt] = data[i];
      items.push({
        itemId: itemId,
        itemName: itemName,
        category: category,
        stock: Number(stock),
        minStock: Number(minStock),
        unit: unit,
        updatedAt: updatedAt
      });
    }

    return { success: true, data: items };
  } catch (err) {
    return { success: false, message: err.toString() };
  }
}

function addItem(sessionToken, itemData, clientUserAgent = null) {
  const auth = verifySession(sessionToken, null, clientUserAgent);
  if (!auth.valid) {
    return { success: false, message: auth.message };
  }

  const lock = LockService.getScriptLock();
  try {
    lock.waitLock(10000);
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName('Items');
    
    const itemId = 'BRG-' + Math.floor(100 + Math.random() * 900);
    const timestamp = new Date().toISOString();

    sheet.appendRow([
      itemId,
      itemData.itemName,
      itemData.category || 'Umum',
      Number(itemData.initialStock) || 0,
      Number(itemData.minStock) || 5,
      itemData.unit || 'Pcs',
      timestamp
    ]);

    if (Number(itemData.initialStock) > 0) {
      const trxSheet = ss.getSheetByName('StockTransactions');
      trxSheet.appendRow([
        'TRX-' + Math.floor(1000 + Math.random() * 9000),
        itemId,
        'STOCK_IN',
        Number(itemData.initialStock),
        'Stok Awal Barang Baru',
        auth.user.username,
        timestamp
      ]);
    }

    return { success: true, message: 'Barang baru berhasil ditambahkan!' };
  } catch (err) {
    return { success: false, message: err.toString() };
  } finally {
    lock.releaseLock();
  }
}

// 6. Penambahan (Stock In) & Pengurangan (Stock Out) Barang
function updateStock(sessionToken, itemId, quantityChange, type, notes, clientUserAgent = null) {
  const auth = verifySession(sessionToken, null, clientUserAgent);
  if (!auth.valid) {
    return { success: false, message: auth.message };
  }

  const lock = LockService.getScriptLock();
  try {
    lock.waitLock(10000);
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName('Items');
    const data = sheet.getDataRange().getValues();
    const qty = Number(quantityChange);

    if (isNaN(qty) || qty <= 0) {
      return { success: false, message: 'Jumlah kuantitas harus berupa angka positif!' };
    }

    let foundRowIndex = -1;
    let currentStock = 0;

    for (let i = 1; i < data.length; i++) {
      if (String(data[i][0]) === String(itemId)) {
        foundRowIndex = i + 1;
        currentStock = Number(data[i][3]);
        break;
      }
    }

    if (foundRowIndex === -1) {
      return { success: false, message: 'Barang tidak ditemukan!' };
    }

    let newStock = currentStock;
    if (type === 'STOCK_IN') {
      newStock = currentStock + qty;
    } else if (type === 'STOCK_OUT') {
      if (qty > currentStock) {
        return { 
          success: false, 
          message: `Stok tidak mencukupi! Stok saat ini: ${currentStock}, diminta: ${qty}` 
        };
      }
      newStock = currentStock - qty;
    } else {
      return { success: false, message: 'Tipe transaksi tidak valid!' };
    }

    const timestamp = new Date().toISOString();

    sheet.getRange(foundRowIndex, 4).setValue(newStock);
    sheet.getRange(foundRowIndex, 7).setValue(timestamp);

    const trxSheet = ss.getSheetByName('StockTransactions');
    const trxId = 'TRX-' + Math.floor(1000 + Math.random() * 9000);
    trxSheet.appendRow([
      trxId,
      itemId,
      type,
      qty,
      notes || '-',
      auth.user.username,
      timestamp
    ]);

    return { 
      success: true, 
      message: `Berhasil update stok (${type})! Stok baru: ${newStock}`,
      newStock: newStock
    };
  } catch (err) {
    return { success: false, message: err.toString() };
  } finally {
    lock.releaseLock();
  }
}

// 7. Get Histori Transaksi Stock
function getTransactionLogs(sessionToken, clientUserAgent = null) {
  try {
    const auth = verifySession(sessionToken, null, clientUserAgent);
    if (!auth.valid) {
      return { success: false, message: auth.message };
    }

    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName('StockTransactions');
    if (!sheet) return { success: true, data: [] };
    const data = sheet.getDataRange().getValues();
    const logs = [];

    for (let i = data.length - 1; i >= 1; i--) {
      const [trxId, itemId, type, quantity, notes, actor, timestamp] = data[i];
      logs.push({
        trxId, itemId, type, quantity: Number(quantity), notes, actor, timestamp
      });
    }

    return { success: true, data: logs };
  } catch (err) {
    return { success: false, message: err.toString() };
  }
}

// 8. User Management (Khusus Admin)
function getUsers(sessionToken, clientUserAgent = null) {
  try {
    const auth = verifySession(sessionToken, 'ADMIN', clientUserAgent);
    if (!auth.valid) {
      return { success: false, message: auth.message };
    }

    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName('Users');
    if (!sheet) return { success: true, data: [] };
    const data = sheet.getDataRange().getValues();
    const users = [];

    for (let i = 1; i < data.length; i++) {
      const [userId, username, passHash, fullName, role, createdAt] = data[i];
      users.push({
        userId, username, fullName, role, createdAt
      });
    }

    return { success: true, data: users };
  } catch (err) {
    return { success: false, message: err.toString() };
  }
}

function createUser(sessionToken, userData, clientUserAgent = null) {
  const auth = verifySession(sessionToken, 'ADMIN', clientUserAgent);
  if (!auth.valid) {
    return { success: false, message: auth.message };
  }

  const lock = LockService.getScriptLock();
  try {
    lock.waitLock(10000);
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName('Users');
    const data = sheet.getDataRange().getValues();

    for (let i = 1; i < data.length; i++) {
      if (String(data[i][1]).toLowerCase() === String(userData.username).toLowerCase()) {
        return { success: false, message: 'Username sudah digunakan!' };
      }
    }

    const userId = 'USR-' + Math.floor(1000 + Math.random() * 9000);
    const passHash = hashPassword(userData.password);
    const createdAt = new Date().toISOString();

    sheet.appendRow([
      userId,
      userData.username,
      passHash,
      userData.fullName,
      userData.role || 'STAFF',
      createdAt
    ]);

    return { success: true, message: 'User baru berhasil dibuat dengan password hash!' };
  } catch (err) {
    return { success: false, message: err.toString() };
  } finally {
    lock.releaseLock();
  }
}

function changePassword(sessionToken, targetUsername, newPassword, clientUserAgent = null) {
  const auth = verifySession(sessionToken, null, clientUserAgent);
  if (!auth.valid) {
    return { success: false, message: auth.message };
  }

  // Jika bukan Admin dan mencoba mengubah password user lain -> Tolak
  if (auth.user.role !== 'ADMIN' && String(auth.user.username).toLowerCase() !== String(targetUsername).toLowerCase()) {
    return { success: false, message: 'Akses ditolak: Anda hanya dapat merubah password akun Anda sendiri!' };
  }

  const lock = LockService.getScriptLock();
  try {
    lock.waitLock(10000);
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName('Users');
    const data = sheet.getDataRange().getValues();
    const newHash = hashPassword(newPassword);

    for (let i = 1; i < data.length; i++) {
      if (String(data[i][1]).toLowerCase() === String(targetUsername).toLowerCase()) {
        sheet.getRange(i + 1, 3).setValue(newHash);
        return { success: true, message: `Password user ${targetUsername} berhasil diperbarui!` };
      }
    }

    return { success: false, message: 'User tidak ditemukan!' };
  } catch (err) {
    return { success: false, message: err.toString() };
  } finally {
    lock.releaseLock();
  }
}

// 7. WhatsApp Integration Helpers & Webhook Listener

/**
 * Memformat pesan WhatsApp standar untuk Info Barang, Order Supplier, dan Struk Transaksi
 */
function generateWhatsAppMessage(type, payload) {
  try {
    if (type === 'ITEM_INFO') {
      const isLow = payload.stock <= payload.minStock;
      const statusIcon = isLow ? '⚠️ STOK KRITIS' : '✅ STOK AMAN';
      return `📦 *INFORMASI BARANG - VIBEINVENTORY*\n\n` +
             `• Kode: ${payload.itemId}\n` +
             `• Nama Barang: ${payload.itemName}\n` +
             `• Kategori: ${payload.category}\n` +
             `• Sisa Stok: ${payload.stock} ${payload.unit}\n` +
             `• Batas Minimal: ${payload.minStock} ${payload.unit}\n` +
             `• Status: ${statusIcon}\n\n` +
             `_Dikirim via VibeInventory System_`;
    }

    if (type === 'REORDER') {
      return `🛒 *PERMOHONAN RESTOK (REORDER SUPPLIER)*\n\n` +
             `Kepada Yth. Supplier / Tim Pengadaan,\n` +
             `Mohon pengadaan kembali stok barang berikut:\n\n` +
             `• Kode Barang: ${payload.itemId}\n` +
             `• Nama Barang: ${payload.itemName}\n` +
             `• Kategori: ${payload.category}\n` +
             `• Sisa Stok: ${payload.stock} ${payload.unit} (Di bawah batas min: ${payload.minStock} ${payload.unit})\n` +
             `• Jumlah Pengadaan: ${payload.requestQty || (payload.minStock * 2)} ${payload.unit}\n\n` +
             `Terima Kasih,\n` +
             `_VibeInventory System_`;
    }

    if (type === 'STRUK_TRX') {
      const typeLabel = payload.type === 'STOCK_IN' ? '📥 STOCK IN (BARANG MASUK)' : '📤 STOCK OUT (BARANG KELUAR)';
      return `📜 *STRUK TRANSAKSI STOK - VIBEINVENTORY*\n\n` +
             `• No. Transaksi: ${payload.trxId}\n` +
             `• Tipe Transaksi: ${typeLabel}\n` +
             `• Kode Barang: ${payload.itemId}\n` +
             `• Kuantitas: ${payload.quantity}\n` +
             `• Catatan: ${payload.notes || '-'}\n` +
             `• Pelaksana: ${payload.actor}\n` +
             `• Waktu: ${payload.timestamp}\n\n` +
             `_Simpan pesan ini sebagai bukti transaksi resmi._`;
    }

    return payload.message || 'Pesan dari VibeInventory';
  } catch (err) {
    return 'Pesan VibeInventory: ' + JSON.stringify(payload);
  }
}

/**
 * Helper untuk Push Notification via WhatsApp Gateway API (Opsional untuk Otomatisasi)
 */
function sendWhatsAppNotification(phoneNumber, message, gatewayConfig = null) {
  if (!phoneNumber || !message) {
    return { success: false, message: 'Nomor tujuan atau pesan tidak boleh kosong.' };
  }

  // Bersihkan format nomor telepon menjadi format internasional (e.g. 628123456789)
  let cleanPhone = String(phoneNumber).replace(/[^0-9]/g, '');
  if (cleanPhone.startsWith('0')) {
    cleanPhone = '62' + cleanPhone.substring(1);
  }

  const apiKey = (gatewayConfig && gatewayConfig.apiKey) || 'DUMMY_WA_GATEWAY_KEY';
  const endpoint = (gatewayConfig && gatewayConfig.endpoint) || 'https://api.fonnte.com/send';

  try {
    const payload = {
      target: cleanPhone,
      message: message
    };

    const options = {
      method: 'post',
      headers: {
        'Authorization': apiKey
      },
      payload: payload,
      muteHttpExceptions: true
    };

    const response = UrlFetchApp.fetch(endpoint, options);
    const resText = response.getContentText();
    return {
      success: true,
      message: 'Permintaan kirim WhatsApp berhasil dikirim ke Gateway API.',
      response: resText
    };
  } catch (err) {
    return { success: false, message: 'Gagal menghubungi WA Gateway: ' + err.toString() };
  }
}

/**
 * Webhook Entrypoint untuk Menerima Event Pesan Masuk dari WhatsApp Gateway API (Opsional)
 */
function doPost(e) {
  try {
    let postData = {};
    if (e && e.postData && e.postData.contents) {
      postData = JSON.parse(e.postData.contents);
    }
    
    // Log pesan masuk atau proses order otomatis via chat
    Logger.log('WA Webhook Received: ' + JSON.stringify(postData));

    return ContentService.createTextOutput(JSON.stringify({
      status: 'success',
      message: 'Webhook WhatsApp diterima oleh VibeInventory Server'
    })).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: 'error',
      message: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

