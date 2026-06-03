// Store the video ID after ingestion
let currentVideoId = null;

// Ingest button click handler
document.getElementById("ingest-btn").addEventListener("click", async () => {
  const url = document.getElementById("video-url").value.trim();
  const status = document.getElementById("ingest-status");

  if (!url) {
    status.textContent = "Please paste a YouTube URL first.";
    return;
  }

  status.textContent = "Ingesting video... please wait.";

  try {
    const response = await fetch("/ingest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url }),
    });

    const data = await response.json();

    if (response.ok) {
      currentVideoId = data.video_id;
      status.textContent = data.message;
    } else {
      status.textContent = `Error: ${data.detail}`;
    }
  } catch (error) {
    status.textContent = "Something went wrong. Please try again.";
  }
});

// Query button click handler
document.getElementById("query-btn").addEventListener("click", async () => {
  const question = document.getElementById("question-input").value.trim();
  const answerBox = document.getElementById("answer-box");

  if (!currentVideoId) {
    answerBox.textContent =
      "Please ingest a video first before asking questions.";
    return;
  }

  if (!question) {
    answerBox.textContent = "Please type a question first.";
    return;
  }

  answerBox.textContent = "Thinking...";

  try {
    const response = await fetch("/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        video_id: currentVideoId,
        question: question,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      answerBox.textContent = data.answer;
      answerBox.classList.add("visible");
    } else {
      answerBox.textContent = `Error: ${data.detail}`;
      answerBox.classList.add("visible");
    }
  } catch (error) {
    answerBox.textContent = "Something went wrong. Please try again.";
  }
});
