/**
 * toast-messages.js
 * Inicializa notificações toast do Bootstrap com auto-dismiss
 * 
 * Funcionalidade:
 * - Converte mensagens Django em toasts Bootstrap
 * - Auto-dismiss após 4 segundos
 * - Animação suave de entrada/saída
 */

document.addEventListener('DOMContentLoaded', function () {
  const toastElements = document.querySelectorAll('.toast-msg');

  if (toastElements.length === 0) return;

  toastElements.forEach(function (el) {
    const toast = new bootstrap.Toast(el, {
      autohide: true,
      delay: 4000
    });
    toast.show();
  });
});
