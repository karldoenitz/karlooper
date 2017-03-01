/**
 * Created by lizhihao on 01/03/2017.
 */

function fill_data(data)
{
    var data_string = "";
    for(var i = 0; i < data.length; i++)
    {
        data_string += data[i]["name"]+"---"+data[i]["gender"]+"---"+data[i]["age"]+"<br/>";
    }
    document.getElementById("users-div").innerHTML = data_string;
}

$(document).ready(
    function()
    {
        $("#Submit").click(
            function()
            {
                $.post(
                    "/user-info",
                    {
                        user_size: Math.ceil(Math.random()*10)
                    },
                    function(data, status)
                    {
                        if(status == 'success')
                        {
                            if('error' in data)
                            {
                                alert(data['error']);
                            }
                            else
                            {
                                fill_data(data["data"])
                            }
                        }
                    }
                );
            }
        );
    }
);
