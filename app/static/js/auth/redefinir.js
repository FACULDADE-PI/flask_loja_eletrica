function send_otp_link() {
    $(document).ready(() => {
        $.ajax({
            method: "POST",
            url: "/auth/reset/password/otp/send",
            data: {
                emailOTP: $("#emailSolicitacaoOTP").val(),
            }
        }).done((data) => {
            // Verifica se a resposta possui um ícone de sucesso
            if (data.hasOwnProperty('icon') && data.icon === 'success') {
                Swal.fire({
                    icon: data.icon,
                    title: data.title,
                    text: data.text
                }).then((result) => {
                    if (result.isConfirmed) {
                        location.reload();
                    }
                });
            } else {
                // Mensagem de erro caso a resposta não tenha um ícone de sucesso
                Swal.fire({
                    icon: 'error',
                    title: 'Erro ao enviar OTP',
                    text: 'Ocorreu um erro ao enviar o OTP. Por favor, tente novamente.'
                });
                // Adiciona um atraso antes de recarregar a página
                setTimeout(() => {
                    location.reload();
                }, 3000); // Espera 3 segundos antes de recarregar
            }
        }).fail(() => {
            // Mensagem de erro em caso de falha na requisição AJAX
            Swal.fire({
                icon: 'error',
                title: 'Erro na solicitação',
                text: 'Houve um erro ao processar sua solicitação. Por favor, tente novamente.'
            });
        });
    });
}
