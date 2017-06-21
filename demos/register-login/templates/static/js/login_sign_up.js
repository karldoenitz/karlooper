/**
 * Created by lizhihao on 01/03/2017.
 */

$(document).ready(
    function()
    {
        $("#id_button_Login").click(
            function()
            {
                $.post(
                    "/rest/login",
                    {
                        user_name: $("#id_username").val(),
                        password: $("#id_password").val()
                    },
                    function(data, status)
                    {
                        if(status === 'success')
                        {
                            if(data["status"] !== 0)
                            {
                                alert(data['message']);
                            }
                            else
                            {
                                alert("Login Successfully!");
                                window.location.href = data["data"]["url"];
                            }
                        }
                    }
                );
            }
        );
    }
);


$(document).ready(
    function()
    {
        $("#id_button_SignUp").click(
            function()
            {
                $.post(
                    "/rest/register",
                    {
                        user_name: $("#id_username").val(),
                        password: $("#id_password").val()
                    },
                    function(data, status)
                    {
                        if(status === 'success')
                        {
                            if(data["status"] !== 0)
                            {
                                alert(data['message']);
                            }
                            else
                            {
                                alert("Sign Up Successfully!");
                                window.location.href = data["data"]["url"];
                            }
                        }
                    }
                );
            }
        );
    }
);
