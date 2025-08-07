function emite_alerta() {
    alert("Python Rocks!");
};

logo = document.getElementsByTagName("img")[0];
logo.onclick = emite_alerta;

window.addEventListener('scroll', function() {
const yOffset = window.pageYOffset;
document.body.style.backgroundPosition = `0px ${yOffset * 0.5}px`;
        
        // Opcional: ajuste para a camada .moving-grid (efeito mais intenso)
        // document.querySelector('.moving-grid').style.backgroundPosition = `0px ${yOffset * 0.8}px`;
});

document.body.style.transform = `perspective(500px) rotateX(${window.scrollY * 0.1}deg)`; 