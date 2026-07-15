const anoAtual = document.getElementById("anoatual");
const ultimaModificacao = document.getElementById("ultimaModificacao");
const menuButton = document.getElementById("menu");
const nav = document.querySelector("nav");
const titulo = document.querySelector("main h1");
const figuras = document.querySelectorAll(".album figure");
const linksFiltro = document.querySelectorAll("nav a[data-filtro]");

anoAtual.textContent = new Date().getFullYear();
ultimaModificacao.textContent = `Última Modificação: ${document.lastModified}`;

menuButton.addEventListener("click", () => {
    nav.classList.toggle("show");
    menuButton.textContent = nav.classList.contains("show") ? "✖" : "☰";
    menuButton.setAttribute(
        "aria-label",
        nav.classList.contains("show") ? "Fechar menu" : "Abrir menu"
    );
});

function filtrarTemplos(filtro) {
    figuras.forEach((figura) => {
        if (filtro === "todos" || figura.classList.contains(filtro)) {
            figura.classList.remove("hide");
        } else {
            figura.classList.add("hide");
        }
    });
}

const titulos = {
    todos: "Álbum do Templo",
    antigo: "Templos Antigos",
    novo: "Templos Novos",
    grande: "Templos Grandes",
    pequeno: "Templos Pequenos"
};

linksFiltro.forEach((link) => {
    link.addEventListener("click", (evento) => {
        evento.preventDefault();
        const filtro = link.dataset.filtro;

        linksFiltro.forEach((item) => item.classList.remove("active"));
        link.classList.add("active");

        titulo.textContent = titulos[filtro] || "Álbum do Templo";
        filtrarTemplos(filtro);

        nav.classList.remove("show");
        menuButton.textContent = "☰";
        menuButton.setAttribute("aria-label", "Abrir menu");
    });
});
