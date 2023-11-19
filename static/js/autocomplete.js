$(document).ready(function(){
    $( "#autocomplete" ).autocomplete({
        source: "/autocomplete"
    });

    $("#search-btn").click(function(){
        $("#search-form").submit();
    });
});