/**
 * location-calc.js
 * Cálculo automático do período de locação e valor total
 * 
 * Funcionalidade:
 * - Ao selecionar data de início e fim, calcula:
 *   1. Quantidade de dias úteis / total
 *   2. Valor total (dias × preço do imóvel)
 * - Exibe o resultado dinamicamente na página
 */

document.addEventListener('DOMContentLoaded', function () {
  const dtStart = document.getElementById('id_dt_start');
  const dtEnd = document.getElementById('id_dt_end');
  const priceDisplay = document.getElementById('location-price');
  const resultContainer = document.getElementById('location-calc-result');

  // Se os elementos não existirem nesta página, não faz nada
  if (!dtStart || !dtEnd || !priceDisplay) return;

  // Cria container de resultado se não existir
  let resultBox = resultContainer || document.createElement('div');
  if (!resultContainer) {
    resultBox.id = 'location-calc-result';
    resultBox.className = 'mt-4 p-3 border rounded bg-light';
    // Insere após o último field do formulário
    const form = dtStart.closest('form');
    if (form) {
      const submitBtn = form.querySelector('input[type="submit"]');
      if (submitBtn) {
        form.insertBefore(resultBox, submitBtn);
      } else {
        form.appendChild(resultBox);
      }
    }
  }

  // Obtém o preço do imóvel (formato BR: R$ 1.500,00)
  const priceText = priceDisplay.textContent.trim();
  // Remove "R$ " e converte para número
  const price = parseFloat(
    priceText
      .replace('R$', '')
      .replace(/\./g, '')
      .replace(',', '.')
      .trim()
  );

  if (isNaN(price)) return;

  function updateCalculation() {
    const startVal = dtStart.value;
    const endVal = dtEnd.value;

    if (!startVal || !endVal) {
      resultBox.innerHTML = `
                <div class="text-muted">
                    <i class="fas fa-info-circle"></i> 
                    Selecione as datas de início e fim para calcular o período e valor total.
                </div>
            `;
      return;
    }

    const start = new Date(startVal + 'T00:00:00');
    const end = new Date(endVal + 'T00:00:00');

    if (end <= start) {
      resultBox.innerHTML = `
                <div class="text-danger">
                    <i class="fas fa-exclamation-triangle"></i> 
                    A data de fim deve ser posterior à data de início.
                </div>
            `;
      return;
    }

    // Calcula diferença em dias
    const diffTime = Math.abs(end - start);
    const totalDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    // Calcula dias úteis (seg-sex)
    let businessDays = 0;
    let current = new Date(start);
    while (current <= end) {
      const dayOfWeek = current.getDay();
      if (dayOfWeek !== 0 && dayOfWeek !== 6) {
        businessDays++;
      }
      current.setDate(current.getDate() + 1);
    }

    // Calcula valor total
    const totalValue = price * totalDays;

    // Formata valores
    const totalValueFormatted = totalValue.toLocaleString('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    });

    const priceFormatted = price.toLocaleString('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    });

    // Exibe resultado
    resultBox.innerHTML = `
            <h5 class="fw-bold mb-3"><i class="fas fa-calculator"></i> Resumo da Locação</h5>
            <div class="row g-2">
                <div class="col-md-6">
                    <table class="table table-sm table-borderless mb-0">
                        <tr>
                            <td class="text-muted">Valor diária:</td>
                            <td class="fw-semibold">${priceFormatted}</td>
                        </tr>
                        <tr>
                            <td class="text-muted">Período total:</td>
                            <td class="fw-semibold">${totalDays} dia(s)</td>
                        </tr>
                        <tr>
                            <td class="text-muted">Dias úteis:</td>
                            <td class="fw-semibold">${businessDays} dia(s)</td>
                        </tr>
                    </table>
                </div>
                <div class="col-md-6 d-flex align-items-center justify-content-center">
                    <div class="text-center">
                        <div class="text-muted small">Valor Total</div>
                        <div class="display-6 fw-bold text-success">${totalValueFormatted}</div>
                    </div>
                </div>
            </div>
            <hr class="my-2">
            <small class="text-muted">
                <i class="fas fa-calendar-alt"></i> 
                ${start.toLocaleDateString('pt-BR')} 
                <i class="fas fa-arrow-right mx-1"></i> 
                ${end.toLocaleDateString('pt-BR')}
                &nbsp;|&nbsp;
                <i class="fas fa-home"></i> 
                ${totalDays} ${totalDays === 1 ? 'diária' : 'diárias'}
            </small>
        `;
  }

  // Atualiza ao mudar as datas
  dtStart.addEventListener('change', updateCalculation);
  dtEnd.addEventListener('change', updateCalculation);

  // Executa uma vez no início se já houver valores
  updateCalculation();
});

