/* accounts/static/js/accounts.js */
$(document).ready(function() {
    // Preview uploaded profile picture
    $("#id_profile_picture").change(function() {
        const [file] = this.files;
        if (file) {
            $("#profilePreview").attr("src", URL.createObjectURL(file));
        }
    });
});