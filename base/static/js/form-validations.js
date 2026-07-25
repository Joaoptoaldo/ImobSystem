/**
 * form-validations.js
 * Validação de formulários no frontend
 * 
 * Funcionalidades:
 * - Máscara de telefone (XX) XXXXX-XXXX
 * - Validação de e-mail
 * - Campos obrigatórios destacados
 * - Validação antes do submit
 * - Feedback visual com Bootstrap
 */

document.addEventListener('DOMContentLoaded', function () {
  initPhoneMask();
  initFormValidations();
});

/**
 * Aplica máscara de telefone (XX) XXXXX-XXXX
 */
function initPhoneMask() {
  const phoneFields = document.querySelectorAll(
    'input[type="text"][name="phone"], input[id*="phone"]'
  );

  phoneFields.forEach(function (input) {
    input.addEventListener('input', function (e) {
      let value = e.target.value.replace(/\D/g, ''); // Remove não-dígitos

      if (value.length > 11) {
        value = value.slice(0, 11);
      }

      if (value.length <= 2) {
        value = '(' + value;
      } else if (value.length <= 7) {
        value = '(' + value.slice(0, 2) + ') ' + value.slice(2);
      } else {
        value =
          '(' +
          value.slice(0, 2) +
          ') ' +
          value.slice(2, 7) +
          '-' +
          value.slice(7);
      }

      e.target.value = value;
    });
  });
}

/**
 * Inicializa validações para todos os formulários na página
 */
function initFormValidations() {
  const forms = document.querySelectorAll('form');

  forms.forEach(function (form) {
    // Adiciona asterisco nos campos obrigatórios
    markRequiredFields(form);

    // Validação no submit
    form.addEventListener('submit', function (e) {
      if (!validateForm(form)) {
        e.preventDefault();
      }
    });

    // Validação em tempo real ao sair do campo (blur)
    const inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(function (input) {
      input.addEventListener('blur', function () {
        validateField(input);
      });
      input.addEventListener('input', function () {
        // Remove estado de erro enquanto digita (se estava com erro)
        if (input.classList.contains('is-invalid')) {
          validateField(input);
        }
      });
    });
  });
}

/**
 * Marca campos obrigatórios com asterisco vermelho
 */
function markRequiredFields(form) {
  const labels = form.querySelectorAll('label');

  labels.forEach(function (label) {
    const input = document.getElementById(label.getAttribute('for'));
    if (input && input.required) {
      if (!label.querySelector('.required-asterisk')) {
        const asterisk = document.createElement('span');
        asterisk.className = 'required-asterisk text-danger ms-1';
        asterisk.textContent = '*';
        label.appendChild(asterisk);
      }
    }
  });

  // Também verifica inputs required sem label com for
  const requiredInputs = form.querySelectorAll('input[required], select[required], textarea[required]');
  requiredInputs.forEach(function (input) {
    // Tenta encontrar a label associada
    const id = input.id;
    let label = null;
    if (id) {
      label = form.querySelector('label[for="' + id + '"]');
    }
    // Se não encontrou label com for, procura a div pai que contém a label
    if (!label) {
      const parent = input.closest('.mt-3') || input.parentElement;
      if (parent) {
        label = parent.querySelector('label');
      }
    }
    if (label && !label.querySelector('.required-asterisk')) {
      const asterisk = document.createElement('span');
      asterisk.className = 'required-asterisk text-danger ms-1';
      asterisk.textContent = '*';
      label.appendChild(asterisk);
    }
  });
}

/**
 * Valida um formulário completo
 */
function validateForm(form) {
  let isValid = true;
  const inputs = form.querySelectorAll(
    'input:not([type="submit"]):not([type="hidden"]):not([type="file"]), select, textarea'
  );

  inputs.forEach(function (input) {
    if (!validateField(input)) {
      isValid = false;
    }
  });

  // Valida campos de arquivo separadamente
  const fileInputs = form.querySelectorAll('input[type="file"]');
  fileInputs.forEach(function (input) {
    if (input.required && !input.files.length) {
      showError(input, 'Este campo é obrigatório.');
      isValid = false;
    }
  });

  return isValid;
}

/**
 * Valida um campo específico e retorna true/false
 */
function validateField(input) {
  // Ignora submits, buttons, hidden
  if (
    input.type === 'submit' ||
    input.type === 'button' ||
    input.type === 'hidden' ||
    input.type === 'file'
  ) {
    return true;
  }

  clearError(input);

  // Se o campo não é obrigatório e está vazio, passa
  if (!input.required && !input.value.trim()) {
    return true;
  }

  let fieldValid = true;
  const value = input.value.trim();
  const name = input.name || input.id || '';

  // 1. Campo obrigatório vazio
  if (input.required && !value) {
    showError(input, 'Este campo é obrigatório.');
    fieldValid = false;
  }

  // 2. Validação de e-mail
  if (fieldValid && (name.includes('email') || input.type === 'email')) {
    if (value && !isValidEmail(value)) {
      showError(input, 'Informe um e-mail válido (ex: nome@dominio.com).');
      fieldValid = false;
    }
  }

  // 3. Validação de telefone
  if (fieldValid && (name.includes('phone') || name.includes('telefone') || name.includes('celular'))) {
    if (value) {
      const digits = value.replace(/\D/g, '');
      if (digits.length < 10 || digits.length > 11) {
        showError(input, 'Informe um telefone válido com DDD (ex: (11) 99999-8888).');
        fieldValid = false;
      }
    }
  }

  return fieldValid;
}

/**
 * Verifica se o e-mail é válido
 */
function isValidEmail(email) {
  const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return re.test(email);
}

/**
 * Exibe mensagem de erro em um campo
 */
function showError(input, message) {
  input.classList.add('is-invalid');

  // Remove feedback existente se houver
  const existingFeedback = input.parentElement.querySelector('.invalid-feedback');
  if (existingFeedback) {
    existingFeedback.textContent = message;
    return;
  }

  const feedback = document.createElement('div');
  feedback.className = 'invalid-feedback';
  feedback.textContent = message;

  // Insere após o input
  if (input.nextSibling) {
    input.parentElement.insertBefore(feedback, input.nextSibling);
  } else {
    input.parentElement.appendChild(feedback);
  }
}

/**
 * Limpa estado de erro de um campo
 */
function clearError(input) {
  input.classList.remove('is-invalid');
  const feedback = input.parentElement.querySelector('.invalid-feedback');
  if (feedback) {
    feedback.remove();
  }
}

