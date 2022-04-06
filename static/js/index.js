function createArticle() {
    let title = document.getElementById("title").value;
    let body = document.getElementById("body").value;

    axios({
        method: "POST",
        url: "/article/create",
        data: {
            title: title,
            body: body,
        },
        headers: {
            "Content-Type": "application/json",
        }
    }).then(
        (response) => {
            let data = response.data;
            if (data.redirect) {
                // redirect exists, then set the URL to the redirect
                window.location.href = data.redirect;
            }

            if (data.status == 500) {
                alert(data.error);
                window.location.href = "/articles";  // redirect to home page
            }
        }
    )
}

function deleteArticle(id, title) {
    let message = "Are you sure you want to delete article with title " + title + "?";
    let confirmDelete = confirm(message);

    if (confirmDelete == true) {
        var url = "/article/" + id + "/delete";

        axios({
            method: 'POST',
            url: url
        }).then(
            (response) => {
                let data = response.data;
                
                if (data.redirect) {
                    window.location.href = data.redirect;
                }
            }
        )
    }
}