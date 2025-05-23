const quotes = [
  "Every new day is a new chance to change your life.",
  "Habits are the path to big achievements, step by step.",
  "Don’t wait for motivation — act, and motivation will follow.",
  "Your discipline is your superpower.",
  "What you do every day shapes who you are.",
  "Small steps every day lead to big results.",
  "Progress, even slow, is better than standing still.",
  "Consistency is stronger than motivation.",
  "The best time to start is now.",
  "Change begins with a simple decision to act.",
  "Success doesn’t come from what you do occasionally, but what you do consistently.",
  "Discipline is choosing between what you want now and what you want most.",
  "Motivation gets you started, habit keeps you going.",
  "Create healthy habits, not restrictions.",
  "You are what you repeatedly do.",
  "Big journeys begin with small steps.",
  "It’s not about being the best, it’s about being better than you were yesterday.",
  "Push yourself, because no one else is going to do it for you.",
  "Stay focused and never give up.",
  "Your only limit is your mind."
];

function showRandomQuoteTemporarily() {
  const quoteElement = document.getElementById("quote");
  const container = document.getElementById("quote-container");

  if (quoteElement && container) {
    const randomIndex = Math.floor(Math.random() * quotes.length);
    quoteElement.textContent = quotes[randomIndex];
    container.style.display = "block"; 

    setTimeout(() => {
      container.style.display = "none"; 
    }, 3000); 
  }
}

document.addEventListener("DOMContentLoaded", showRandomQuoteTemporarily);
