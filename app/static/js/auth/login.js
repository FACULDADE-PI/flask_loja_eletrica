



function logar_usuario() {
    // solicitação de login
    event.preventDefault();

    $(document).ready(() => {
        $.ajax({
            method: "POST",
            url: "/auth/login/user",
            data: {
                email_usuario: $("#email_usuario").val(),
                senha_usuario: $("#senha_usuario").val(),
            }
        }).done((data) => {
            if (data.hasOwnProperty('icon') && data['icon'] == 'success') {
                // Redirecionar para a página inicial
                window.location.href = "/";
            } else {
                Swal.fire(data);
            }
        });
    });
}



function redirect_register() {
    //solicitacao_novo_cadastro
    event.preventDefault()
    $(document).ready(()=>{
        window.location.href = "register";
    });
}


