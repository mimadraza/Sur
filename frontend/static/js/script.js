function setGradient(angle, color1, color2) {
    document.body.style.background = `linear-gradient(${angle}, ${color1}, ${color2})`;
}

function animateGradient() {
    let i = 0;
    setInterval(() => {
        const color1 = colors[i % colors.length];
        const color2 = colors[(i + 1) % colors.length];
        setGradient('35deg', color1, color2);
        i++;
    }, 200); // Changes gradient every 2 seconds
}

window.onload = animateGradient;
