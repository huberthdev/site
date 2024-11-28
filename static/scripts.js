document.addEventListener('DOMContentLoaded', function () {
    const phoneInput = document.getElementById('phone');
    const form = document.getElementById('frmMain');

    if (phoneInput) {
        phoneInput.addEventListener('input', function (e) {
            let value = e.target.value.replace(/\D/g, '');

            if (value.length > 0) {
                if (value.length <= 2) {
                    value = `(${value}`;
                } else if (value.length <= 7) {
                    value = `(${value.substring(0, 2)}) ${value.substring(2)}`;
                } else {
                    value = `(${value.substring(0, 2)}) ${value.substring(2, 7)}-${value.substring(7, 11)}`;
                }
            }

            e.target.value = value;
        });

        phoneInput.addEventListener('blur', function (e) {
            const value = e.target.value.replace(/\D/g, '');
            if (value.length < 10 || value.length > 11) {
                alert('Por favor, insira um número válido com DDD e telefone completo.');
                e.target.value = '';
            }
        });
    } else {
        console.error("Campo de telefone não encontrado. Verifique o ID do campo.");
    }

    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const phoneValue = phoneInput.value.replace(/\D/g, '');
            if (phoneValue.length < 10 || phoneValue.length > 11) {
                alert('Número de telefone inválido!');
                return;
            }

            let formData = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                phone: phoneInput.value,
                description: document.getElementById('description').value
            };

            fetch('/api/cotacao', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    showModal(data.message);

                    form.reset();
                } else if (data.error) {
                    alert('Erro: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                alert('Houve um erro ao enviar o orçamento. Tente novamente.');
            });
        });
    } else {
        console.error("Formulário não encontrado. Verifique o ID do formulário.");
    }

    function showModal(message) {
        const modal = document.getElementById('successModal');
        const modalContent = modal.querySelector('.modal-content p');
        modalContent.textContent = message;

        modal.style.display = 'flex';

        const closeButton = modal.querySelector('.close');
        closeButton.onclick = function() {
            modal.style.display = 'none';
        };

        window.onclick = function(event) {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        };

        setTimeout(function() {
            modal.style.display = 'none';
        }, 5000);
    }

    window.onload = function() {
        const currentUrl = window.location.href;
        const baseUrl = window.location.origin + window.location.pathname;

        if (currentUrl !== baseUrl) {
            window.history.replaceState({}, document.title, baseUrl);
        }
    };

    let lastScrollY = window.scrollY;

    window.addEventListener('scroll', () => {
        const socialBar = document.querySelector('.social-bar');
        if (window.scrollY > lastScrollY) {
            socialBar.classList.add('hidden');
        } else {
            socialBar.classList.remove('hidden');
        }
        lastScrollY = window.scrollY;
    });
});
