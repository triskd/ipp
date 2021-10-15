<?php 
	
	class Killer{

		public function __construct($errNum,  $errLog){

			fwrite(STDERR, $errLog . PHP_EOL);
			fwrite(STDERR, "Navratovy kod: ".$errNum. PHP_EOL);
			exit($errNum);			

		}

	}



 ?>