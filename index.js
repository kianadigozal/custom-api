const express = require('express');
const app = express();

// Enable CORS for all routes
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});

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

// For Vercel serverless deployment
if (process.env.NODE_ENV !== 'production') {
  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
  });
}

module.exports = app; 