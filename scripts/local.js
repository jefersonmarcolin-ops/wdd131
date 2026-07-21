const temperatura = 8;
const velocidadeVento = 18;

function calcularSensacaoTermica(temp, vento) {
    return 13.12 + 0.6215 * temp - 11.37 * Math.pow(vento, 0.16) + 0.3965 * temp * Math.pow(vento, 0.16);
}

const saida = document.getElementById("sensacao");

if (temperatura <= 10 && velocidadeVento > 4.8) {
    saida.textContent = `${calcularSensacaoTermica(temperatura, velocidadeVento).toFixed(1)} °C`;
} else {
    saida.textContent = "N/A";
}

document.getElementById("anoatual").textContent = new Date().getFullYear();
document.getElementById("ultimaModificacao").textContent =
    `Última Modificação: ${document.lastModified}`;
