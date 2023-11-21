function send_otp_link() {
    $(document).ready(() => {
        // Obtém o valor do campo de email
        let email = $("#emailSolicitacaoOTP").val();

        // Expressão regular para validar o formato do email
        let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        // Verifica se o campo de email está vazio ou não corresponde ao formato de email válido
        if (!email || !emailRegex.test(email)) {
            Swal.fire({
                icon: 'error',
                title: 'Email inválido',
                text: 'Por favor, insira um endereço de email válido.'
            });
            return; // Retorna para evitar a execução do AJAX
        }

        // Se o email for válido, continua com a chamada AJAX
        $.ajax({
            method: "POST",
            url: "/auth/reset/password/otp/send",
            data: {
                emailOTP: email,
            }
        }).done((data) => {
            Swal.fire({
                icon: data.icon,
                title: data.title,
                text: data.text
            })
        }).fail(() => {
            // Mensagem de erro em caso de falha na requisição AJAX
            Swal.fire({
                icon: 'error',
                title: 'Erro na solicitação',
                text: 'Houve um erro ao processar sua solicitação. Por favor, tente novamente.'
            });
        });
    });

    // Evitar o recarregamento da página após enviar o formulário
    event.preventDefault();
}


function redefine_my_password(event) {
    event.preventDefault(); // Evitar o recarregamento da página após enviar o formulário
    $(document).ready(() => {
        // Obtém o valor do campo de senha
        let newPassword = $("#newPassword").val();

        // Expressão regular para validar a senha (mínimo de 6 caracteres, sem espaços)
        let passwordRegex = /^(?=\S{6,}$).*/;

        // Verifica se a senha é válida
        if (!passwordRegex.test(newPassword)) {
            Swal.fire({
                icon: 'error',
                title: 'Senha inválida',
                text: 'A senha deve ter no mínimo 6 caracteres e não pode conter espaços.'
            });
            return; // Retorna para evitar a execução do AJAX
        }

        // Se a senha for válida, continua com a chamada AJAX
        $.ajax({
            method: "POST",
            url: "/auth/reset/password/completion",
            data: {
                newPassword: newPassword,
                token: window.location.href.split("token=")[1]
            }
        }).done((data) => {
            Swal.fire(data).then((result) => {
                // Se o ícone for sucesso e o usuário clicar em OK, redireciona para "/"
                if (data.hasOwnProperty('icon') && data.icon === 'success' && result.isConfirmed) {
                    window.location.href = "/"; // Redireciona para a página inicial
                }
            });
        }).fail(() => {
            Swal.fire({
                icon: 'error',
                title: 'Erro na solicitação',
                text: 'Houve um erro ao processar sua solicitação. Por favor, tente novamente.'
            });
        });
    });
}
