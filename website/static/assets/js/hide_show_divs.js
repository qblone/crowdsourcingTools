 $(document).ready(function() {
    $("input[name$='rg']").click(function() {
        var test = $(this).val();

        $("div.desc").hide();
        $("#proceed" + test).show();
    });
});

