# 🎓 Rollmates Thread (XX05150)

If your roll ends with **05150**, you're one of us.  
Submit your JSON message and be part of this forever thread!

➡️ [Live Visual Thread](https://shuvodipdassowmik.github.io/XX05150-Thread/)

![Contributors](https://contrib.rocks/image?repo=shuvodipdassowmik/XX05150-Thread)

---

## 🔧 How to Submit

1. Fork this repo  
2. Create a file in `/submissions` named like `2105150.json`  
3. Fill it like:

```json
{
  "roll": "XX05150",
  "name": "Your Name",
  "message": "Your message",
  "email": "Your email",
  "facebook": "Your Facebook ID URL"
}
```

4. Commit and submit a pull request.  

---

## 📅 Timeline
See the evolution here: [`Timeline.md`](./Timeline.md)

---

## 🛠 Development

Files are automatically updated via GitHub Actions when new submissions are added.

To generate files locally:

```bash
# Generate thread files
python scripts/generate_thread.py
python scripts/generate_timeline.py
```

Local testing: Open `index.html` or run `python -m http.server` to serve files.
