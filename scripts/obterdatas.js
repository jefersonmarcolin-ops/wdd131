const anoAtual = document.getElementById("anoatual");
const ultimaModificacao = document.getElementById("ultimaModificacao");

anoAtual.textContent = new Date().getFullYear();
ultimaModificacao.textContent = `Última Modificação: ${document.lastModified}`;
