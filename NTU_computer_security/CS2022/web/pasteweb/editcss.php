<?php
  session_start();
  if(!isset($_SESSION['name'])){
    header("Location: /");
    die();
  }
  // When you see this line, you probably don't need to read 'lessc.inc.php', the intended sollution of flag 3 have nothing to do with it
  require "lessc.inc.php";
  $less = new lessc;

	$sandbox = './sandbox/'.md5($_SESSION['name']).'/';
	if (!file_exists($sandbox)){
		mkdir($sandbox);
	}
	chdir($sandbox);

  if($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['less'])){
		file_put_contents('input.less', $_POST['less']);
		$theme = isset($_POST['theme'])? str_replace('/', '', $_POST['theme']): 'default';
		$less->compileFile('input.less', $theme.'.css');;
		$_SESSION['message'] = "CSS updated successfully!";
  }
?>


<!DOCTYPE html>
<html>
<head>
	<title>Edit <?=$_SESSION['name'];?>'s website</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://unpkg.com/@tailwindcss/forms@0.2.1/dist/forms.min.css" rel="stylesheet">
  <style>
    body{
      height: 100vh;
    }
  </style>
  <script>setTimeout(()=>message.remove(), 3000)</script>
</head>
  <body class="bg-gray-900">

		<nav class="border-gray-200 px-2 sm:px-4 py-2.5 rounded dark:bg-gray-900">
			<div class="container flex flex-wrap items-center justify-between mx-auto">
				<a href="/" class="flex items-center">
						<span class="self-center text-xl font-semibold whitespace-nowrap dark:text-white">PasteWeb</span>
				</a>
				<div class="hidden w-full md:block md:w-auto" id="navbar-default">
					<ul class="flex flex-col p-4 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:flex-row md:space-x-8 md:mt-0 md:text-sm md:font-medium md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
						<li>
							<a href="/edithtml.php" class="block py-2 pl-3 pr-4 text-gray-700 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-gray-400 md:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">Edit HTML</a>
						</li>
						<li>
							<a href="/editcss.php" class="block py-2 pl-3 pr-4 text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-white" aria-current="page">Edit CSS</a>
						</li>
						<li>
							<a href="/view.php" class="block py-2 pl-3 pr-4 text-gray-700 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-gray-400 md:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">View</a>
						</li>
						<li>
							<a href="/share.php" class="block py-2 pl-3 pr-4 text-gray-700 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-gray-400 md:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">Share</a>
						</li>
						<li>
							<a href="/download.php" class="block py-2 pl-3 pr-4 text-gray-700 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-gray-400 md:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">Download</a>
						</li>
					</ul>
				</div>
			</div>
		</nav>

    <div class="flex justify-center items-center mt-10">
			<div class="min-w-[90%] bg-slate-200 py-8 px-8 drop-shadow rounded-xl">
        <h2 class="text-2xl font-bold text-black">Edit CSS (Support LESS)</h2>
        <div class="mt-8">
          <form class="grid grid-cols-1 gap-6" method="POST" id="form">
            <label class="block">
							<textarea name="less" rows="30" class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-slate-300 dark:border-gray-600 dark:placeholder-gray-800 dark:text-black dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Write your CSS/LESS here..."></textarea>
            </label>
            <button class="py-2 text-white bg-slate-500 rounded drop-shadow-lg justify-self-end" style="width: 64px">
              Save
            </button>
          </form>
        </div>
      </div>
    </div>
  </body>
	<?php if(isset($_SESSION['message'])): ?>
		<div id="message" class="bg-green-100 border-l-4 border-green-500 text-green-700 p-4" role="alert" style="position: fixed; top: 1em; right: 1em;">
			<p class="font-bold">Hi, <?=htmlentities($_SESSION['name'])?></p>
			<p><?php echo htmlentities($_SESSION['message']); unset($_SESSION['message']);?></p>
		</div>
	<?php endif; ?>
</html>
