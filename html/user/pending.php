<?php
    require_once("util.inc");
    require_once("db.inc");

    // show results with pending credit for this user

    db_init();
    $user = get_logged_in_user();
    page_head("Pending credit", $user);
    $res = mysql_query("select * from result where userid=$user->id and validate_state=0");
    $sum = 0;
    start_table();
    echo "<tr><th>Result ID</th><th>Claimed credit</th></tr>\n";
    while ($result = mysql_fetch_object($res)) {
        if ($result->claimed_credit > 0) {
            echo "<tr><td>$result->id</td><td>",format_credit($result->claimed_credit), "</td></tr>\n";
            $sum += $result->claimed_credit;
        }
    }
    end_table();

    echo "Pending credit: ",format_credit($sum);
    page_tail();
?>
