const starsContainer = document.querySelector('.stars');

for (let i = 0; i < 100; i++) {
  const star = document.createElement('div');
  star.classList.add('star');
  star.style.left = `${Math.random() * 100}vw`;
  star.style.top = `${Math.random() * 100}vh`;
  star.style.animationDelay = `${Math.random() * 5}s`;
  star.style.animationDuration = `${1.5 + Math.random() * 3}s`;
  starsContainer.appendChild(star);
}