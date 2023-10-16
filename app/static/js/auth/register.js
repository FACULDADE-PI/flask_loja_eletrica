function registrar_usuario() {
    //solicitacao_novo_cadastro
    event.preventDefault()
    $(document).ready(()=>{
        $.ajax({
            method: "POST",
            url: "/auth/register/new",
            data: {
                nome_usuario: $("#nome_usuario").val(),
                email_usuario: $("#email_usuario").val(),
                senha_usuario_1: $("#senha_usuario_1").val(),      
                senha_usuario_2: $("#senha_usuario_2").val(),      
            }
        }).done((data)=> {
            Swal.fire(
                data
            ).then(function() {
                if (data.hasOwnProperty('icon') && data['icon'] == 'success'){
                    window.location.href="/"
                }
            });
        });
    });
}
