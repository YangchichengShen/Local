// src/pages/api/gemini.js
import axios from 'axios';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Only POST requests allowed' });
  }

  const { prompt } = req.body;
  const API_KEY = process.env.GEMINI_API_KEY;

  if (!API_KEY) {
    return res.status(500).json({ message: 'Missing Gemini API Key' });
  }

  try {
    const response = await axios.post(
      `https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key=${API_KEY}`,
      {
        contents: [
          { parts: [{ text: prompt }] }
        ]
      }
    );

    const resultText = response.data.candidates[0]?.content?.parts[0]?.text || '';

    res.status(200).json({ text: resultText });
  } catch (error) {
    console.error('Gemini API Error:', error.response?.data || error.message);
    res.status(500).json({ message: 'Error calling Gemini API' });
  }
}
