<?php
  // Here is your second FLAG: FLAG{a_l1tTl3_tRicKy_.git_L34k..or_D1d_y0u_f1nD_a_0Day_1n_lessphp?}
  session_start();
  if(isset($_SESSION['name'])){
    header("Location: /edithtml.php");
    die();
  }
  $now = new DateTime();
  $getenv = "getenv"; $md5 = "md5";
  $dbconn = pg_connect("host=db dbname={$getenv("POSTGRES_DB")} user={$getenv("POSTGRES_USER")} password={$getenv("POSTGRES_PASSWORD")}");

  if($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['username']) && isset($_POST['password']) && isset($_POST['current_time'])){
    if(abs($now->getTimestamp() - intval($_POST['current_time'])) > 10){
      $_SESSION['message'] = "When do you came from?";
      header("Location: /");
      die();
    }

    $result = pg_query("SELECT user_account, user_password FROM pasteweb_accounts WHERE user_password='{$md5($_POST["password"])}' AND user_account='{$_POST["username"]}';"); 
    if(!pg_num_rows($result)){
      $_SESSION['message'] = "Login Failed";
      header("Location: /");
      die();
    }

    $user = pg_fetch_row($result);
    if($user[0] !== $_POST["username"]){
      $_SESSION['message'] = "Bad Hacker!";
      header("Location: /");
      die();
    }

    $_SESSION['name'] = $user[0];
    header("Location: /edithtml.php");
    die();
  }
?>


<!DOCTYPE html>
<html>
<head>
  <title>PasteWeb</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://unpkg.com/@tailwindcss/forms@0.2.1/dist/forms.min.css" rel="stylesheet">
  <style>
    body{
      height: 100vh;
    }
  </style>
  <script>
    setTimeout(()=>message.remove(), 3000);
    setInterval(()=>current_time.value = parseInt(current_time.value)+1, 1000);
  </script>
</head>
  <body class="bg-gray-900">
    <div class="flex justify-center items-center h-full">
      <div class="min-w-[25%] bg-slate-200 py-12 px-8 drop-shadow rounded-xl">
        <h2 class="text-2xl font-bold text-slate-800">Login</h2>
        <div class="mt-8">
          <form class="grid grid-cols-1 gap-6" method="POST" id="form">
            <label class="block">
              <span class="text-slate-800">Username</span>
              <input name="username" type="text" class="block w-full mt-1" placeholder="" />
            </label>
            <label class="block">
              <span class="text-slate-800">Password</span>
              <input name="password" type="password" class="block w-full mt-1" placeholder=""/>
            </label>
            <input id="current_time" name="current_time" hidden value="<?=$now->getTimestamp();?>"/>
            <button class="block mt-4 py-2 text-white bg-slate-500 rounded shadow-lg shadow-slate-300">
              Login
            </button>
          </form>
        </div>
      </div>
    </div>
  </body>
	<?php if(isset($_SESSION['message'])): ?>
		<div id="message" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4" role="alert" style="position: fixed; top: 1em; right: 1em;">
			<p class="font-bold">Error</p>
			<p><?php echo htmlentities($_SESSION['message']); unset($_SESSION['message']);?></p>
		</div>
	<?php endif; ?>
</html>