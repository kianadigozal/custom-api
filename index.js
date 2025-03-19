const express = require('express');
const app = express();
const axios = require('axios'); // برای ارسال درخواست HTTP
const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');

// Enable CORS for all routes
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});

// ایجاد پوشه temp اگر وجود نداشته باشد
const tempDir = path.join(__dirname, 'temp');
fs.mkdir(tempDir, { recursive: true }).catch(console.error);

// تابع ایجاد نام تصادفی برای فایل
function generateRandomFileName() {
  return crypto.randomBytes(16).toString('hex') + '.png';
}

// تابع حذف فایل بعد از مدت زمان مشخص
async function deleteFileAfterDelay(filePath, delayMs) {
  try {
    await new Promise(resolve => setTimeout(resolve, delayMs));
    await fs.unlink(filePath);
    console.log(`File deleted: ${filePath}`);
  } catch (error) {
    console.error(`Error deleting file ${filePath}:`, error);
  }
}

// Greeting endpoint
app.get('/api/greet', (req, res) => {
  const firstName = req.query.firstName;
  const lastName = req.query.lastName;
  
  if (!firstName || !lastName) {
    return res.status(400).json({ 
      error: 'نام و نام خانوادگی الزامی است'
    });
  }
  
  return res.json({
    message: `سلام ${firstName} ${lastName}`
  });
});

// Random number endpoint
app.get('/api/random', (req, res) => {
  const randomNumber = Math.floor(Math.random() * 10) + 1; // تولید عدد تصادفی بین 1 تا 10
  return res.json({
    number: randomNumber
  });
});

// Image generation endpoint
app.get('/api/image', async (req, res) => {
  try {
    const query = req.query.q || 'dog'; // اگر پارامتر ارسال نشده باشد، از 'dog' استفاده می‌کند
    const response = await axios.get(`https://open.wiki-api.ir/apis-1/MakePhotoAi?q=${encodeURIComponent(query)}`);
    
    if (response.data.status && response.data.results.img) {
      // دریافت تصویر از آدرس ارائه شده
      const imageResponse = await axios.get(response.data.results.img, { responseType: 'arraybuffer' });
      
      // ایجاد نام تصادفی برای فایل
      const randomFileName = generateRandomFileName();
      const filePath = path.join(tempDir, randomFileName);
      
      // ذخیره فایل
      await fs.writeFile(filePath, imageResponse.data);
      console.log(`File saved: ${filePath}`);
      
      // تنظیم حذف فایل بعد از 120 ثانیه
      deleteFileAfterDelay(filePath, 120000); // 120000 milliseconds = 120 seconds
      
      // ارسال فایل به کاربر
      res.setHeader('Content-Type', 'image/png');
      res.setHeader('Cache-Control', 'no-cache');
      const fileStream = await fs.readFile(filePath);
      res.send(fileStream);
    } else {
      return res.status(400).json({
        error: 'خطا در دریافت تصویر از سرویس Wiki-Api'
      });
    }
  } catch (error) {
    console.error('Error:', error.message);
    return res.status(500).json({
      error: 'خطا در پردازش درخواست'
    });
  }
});

// For Vercel serverless deployment
if (process.env.NODE_ENV !== 'production') {
  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
  });
}

module.exports = app; 