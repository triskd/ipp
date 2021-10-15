<?php 
	
	require_once("Instr.php");
	require_once("Killer.php");

	class Prog{

		public $instrSet = [];

		public $inputLines = [];
		public $program = [];			//pole zkontrolovanych instrukci
		public $FLAGS = [];
		public $STATP = Array(
			"file"	 => "",
			"loc" 	 =>	0,
			"comm"	 => 0,
			"jump"	 => 0,
			"labels" => []
		);


		public function __construct($args){

			$STATPFlags = [];
			$STATPFile = "";
			$STATPFileBool = false;
			$STATP = false;
			$help = false;

			foreach ($args as $key => $arg) {
				
				if($arg == "--help"){
					$help = true;
				}

				if($arg == "--loc" || $arg == "--jumps" || $arg == "--labels" ||  $arg == "--comments"){
					$STATP = true;
					array_push($STATPFlags, $arg);
				}

				if(preg_match("/(--stats=)(.*)/", $arg, $decode)){

					if($STATPFileBool == false){
						
						if(isset($decode[2]) && $decode[2] != ""){
						
							$STATPFile = $decode[2];
							$STATPFileBool = true;
						
						}else{
							
							new Killer(10, "Argument '--stats='  zadan bez prislusneho souboru!");

						}

					}else{

						new Killer(10, "Argument '--stats=' zadan vicekrat!");

					}

				}

			}



			if($help && ($STATP || $STATPFileBool)){
			
				new Killer(10, "Zakazana kombinace argumentu\n - argument '--help' nelze kombinovat s zadnymi dalsim argumenty!");
			
			}else if($help){

				echo "Napoveda scriptu parse.php - lexikalni a syntakticky analyzator jazyka IPPcode20\n".
					"-----------------------------------------------------------------------------------------------------\n".
					" - autor: David Triska, xtrisk05, 2020\n".
					' - spusteni: $ php7.4 parse.php <seznam_argumentu>  < <vstupni_program>'.PHP_EOL.
					" - vstup: STDIN zdrojovy program v jazyce IPPcode20\n".
					" - vystup: STDOUT XML reprezentace zdrojoveho programu\n".
					" \n- argumenty programu: \n".
					"    --help\n".
					"      - script nenacita zadny vstup, pouze vypisuje napovedu\n".
					"      - tento argument nelze kombinovat s zadnym jinym!\n\n".
					'    --stats="<file>"'.PHP_EOL.      
					"      - <file> sobor do ktereho se vypise statistiky zdrojoveho programu\n".
					"      - argument lze kombinavat s nasledujicimi argumenty: \n            --loc, --jumps, --labels, --coments\n".
					"      - spusteni scriptu s nekterym z predchozich argumentu bez argumentu --stats=<file>  nelze!\n".
					"-----------------------------------------------------------------------------------------------------\n";

				exit(0);

			}

			if(sizeof($STATPFlags) > 0 && !$STATPFileBool){
				new Killer(10, "Zakazana kombinace argumentu\n - chyby argument '--stats='!");
			}

			if($STATPFile != ""){

				if($file = fopen($STATPFile, 'w')){

				}else{
					new Killer(12, "Chyba pri otevirani vystupniho souboru pro zapis statistik");

				}
				
			}
			

			$this->setInstrTypeSet();
			$this->readStdin();
			$this->decodeLines();
			$this->generateXML();

			$statsEcho = "";

			foreach ($STATPFlags as $key => $value) {
				
				switch($value){

					case "--loc":
						
						$statsEcho = $statsEcho.$this->STATP["loc"]."\n";

					break;

					case "--jumps":
						$statsEcho = $statsEcho.$this->STATP["jump"]."\n";
					break;

					case "--comments":
						$statsEcho = $statsEcho.$this->STATP["comm"]."\n";
					break;

					case "--labels":
						$statsEcho = $statsEcho.sizeof($this->STATP["labels"])."\n";
					break;

				}

			}

			if(isset($file)){
				fwrite($file, $statsEcho);
				fclose($file);
	
			}

			
		}

		private function setInstrTypeSet(){


			//instrukce majici 0 parametru
			array_push($this->instrSet, new InstrType("RETURN", 0));		
			array_push($this->instrSet, new InstrType("BREAK", 0));		
			array_push($this->instrSet, new InstrType("POPFRAME", 0));		
			array_push($this->instrSet, new InstrType("PUSHFRAME", 0));	
			array_push($this->instrSet, new InstrType("CREATEFRAME", 0));	

			//instrukce majici 1 parametr
			array_push($this->instrSet, new InstrType("DEFVAR", 1));	$last = end($this->instrSet); $last->setArgTypes(["var"]); // var menim na type
			array_push($this->instrSet, new InstrType("CALL", 1));		$last = end($this->instrSet); $last->setArgTypes(["label"]);
			array_push($this->instrSet, new InstrType("PUSHS", 1));		$last = end($this->instrSet); $last->setArgTypes(["symb"]);
			array_push($this->instrSet, new InstrType("POPS", 1));		$last = end($this->instrSet); $last->setArgTypes(["var"]);	
			array_push($this->instrSet, new InstrType("WRITE", 1));		$last = end($this->instrSet); $last->setArgTypes(["symb"]);
			array_push($this->instrSet, new InstrType("LABEL", 1));		$last = end($this->instrSet); $last->setArgTypes(["label"]);
			array_push($this->instrSet, new InstrType("JUMP", 1));		$last = end($this->instrSet); $last->setArgTypes(["label"]);
			array_push($this->instrSet, new InstrType("EXIT", 1));		$last = end($this->instrSet); $last->setArgTypes(["symb"]);
			array_push($this->instrSet, new InstrType("DPRINT", 1));	$last = end($this->instrSet); $last->setArgTypes(["symb"]);

			//instrukce majici 2 parametry
			array_push($this->instrSet, new InstrType("MOVE", 2));		$last = end($this->instrSet); $last->setArgTypes(["var", "symb"]);
			array_push($this->instrSet, new InstrType("INT2CHAR", 2)); 	$last = end($this->instrSet); $last->setArgTypes(["var", "symb"]);
			array_push($this->instrSet, new InstrType("READ", 2)); 		$last = end($this->instrSet); $last->setArgTypes(["var", "type"]);
			array_push($this->instrSet, new InstrType("STRLEN", 2)); 	$last = end($this->instrSet); $last->setArgTypes(["var", "symb"]);
			array_push($this->instrSet, new InstrType("TYPE", 2)); 		$last = end($this->instrSet); $last->setArgTypes(["var", "symb"]);
			array_push($this->instrSet, new InstrType("NOT", 2)); 		$last = end($this->instrSet); $last->setArgTypes(["var", "symb"]);

			//instrukce majici 3 parametry
			array_push($this->instrSet, new InstrType("ADD", 3));		$last = end($this->instrSet); $last->setArgTypes(["var", "symb", "symb"]);
			array_push($this->instrSet, new InstrType("SUB", 3));		$last = end($this->instrSet); $last->setArgTypes(["var", "symb", "symb"]);
			array_push($this->instrSet, new InstrType("MUL", 3));		$last = end($this->instrSet); $last->setArgTypes(["var", "symb", "symb"]);
			array_push($this->instrSet, new InstrType("IDIV", 3));		$last = end($this->instrSet); $last->setArgTypes(["var", "symb", "symb"]);
			array_push($this->instrSet, new InstrType("LT", 3));		$last = end($this->instrSet); $last->setArgTypes(["var", "symb", "symb"]);
			array_push($this->instrSet, new InstrType("GT", 3));		$last = end($this->instrSet); $last->setArgTypes(["var", "symb", "symb"]);
			array_push($this->instrSet, new InstrType("EQ", 3));		$last = end($this->instrSet); $last->setArgTypes(["var", "symb", "symb"]);
			array_push($this->instrSet, new InstrType("AND", 3));		$last = end($this->instrSet); $last->setArgTypes(["var", "symb", "symb"]);
			array_push($this->instrSet, new InstrType("OR", 3));		$last = end($this->instrSet); $last->setArgTypes(["var", "symb", "symb"]);
			array_push($this->instrSet, new InstrType("STRI2INT", 3));	$last = end($this->instrSet); $last->setArgTypes(["var", "symb", "symb"]);
			array_push($this->instrSet, new InstrType("CONCAT", 3)); 	$last = end($this->instrSet); $last->setArgTypes(["var", "symb", "symb"]);
			array_push($this->instrSet, new InstrType("GETCHAR", 3)); 	$last = end($this->instrSet); $last->setArgTypes(["var", "symb", "symb"]);
			array_push($this->instrSet, new InstrType("SETCHAR", 3)); 	$last = end($this->instrSet); $last->setArgTypes(["var", "symb", "symb"]);
			array_push($this->instrSet, new InstrType("JUMPIFEQ", 3));	$last = end($this->instrSet); $last->setArgTypes(["label", "symb", "symb"]);
			array_push($this->instrSet, new InstrType("JUMPIFNEQ", 3));	$last = end($this->instrSet); $last->setArgTypes(["label", "symb", "symb"]);

		}

		private function readStdin(){

			while($stdl = fgets(STDIN)){
				array_push($this->inputLines, $stdl);
			}


		}

		private function decodeLines(){


			foreach ($this->inputLines as $line => $lineValue) {

				if($line == 0){
				//kontrola hlavicky
					if(preg_match('/^\s*(.ippcode20)(\s*(#)+.*)?\s*$/i', $lineValue, $matches)){
					
						//zapocteni komentare
						if(sizeof($matches) >= 3){
							
							if($matches[3] == '#'){
								$this->STATP["comm"] += 1;
							}								
							
						}
								
					}else{

						new Killer(21, "Chybna hlavicka");

					}
					
										
				}else{
				//dekoddovani tela programu

					$found = false;

					//prazdny radek
					if(preg_match("/^\s*$/", $lineValue, $matches)){
						$found = true;	
					}

					//samotny komentar na radku
					if(preg_match('/^\s*#+.*$/', $lineValue, $matches)){

						$this->STATP["comm"] += 1;
						$found = true;
					}


					//validni operacni kod, pripadny komentar
					if(preg_match('/^\s*(\w+)/i', $lineValue, $matches)){
						
						$found = false;
						//print_r($matches);
						foreach ($this->instrSet as $key => $instrType) {
								
							//pokud ji ze nalezeny validni opcode, ukoci hledani
							if($found == true){
								break;
							}							

							if(strtolower($instrType->opcode) == strtolower($matches[1])){
								
								$this->STATP["loc"] += 1;
								$found = true;


								switch ($instrType->argc) {
									
									case 0:
										array_push($this->program, new Instr0Arg($instrType, $lineValue, $line+1, $this->STATP["loc"]) );
									break;
								
									case 1:
										array_push($this->program, new Instr1Arg($instrType, $lineValue, $line+1, $this->STATP["loc"]) );
									break;

									case 2:
										array_push($this->program, new Instr2Arg($instrType, $lineValue, $line+1, $this->STATP["loc"]) );
									break;

									case 3:
										array_push($this->program, new Instr3Arg($instrType, $lineValue, $line+1, $this->STATP["loc"]) );
									break;

								}

								$lastInstr = end($this->program);
								$lastInstr->analyze();

								//STATP --labels
								if($lastInstr->instrType->opcode == "LABEL"){
									array_push($this->STATP["labels"], $lastInstr->argv[0]);
									array_unique($this->STATP["labels"]);
								}

								//STATP --comments
								if($lastInstr->comm == true){
									$this->STATP["comm"] += 1;
								}

								//STATP --jumps
								if($lastInstr->instrType->opcode == "JUMP" || $lastInstr->instrType->opcode =="JUMPIFEQ" || $lastInstr->instrType->opcode =="JUMPIFNEQ" || $lastInstr->instrType->opcode == "CALL" || $lastInstr->instrType->opcode == "RETURN"){

									$this->STATP["jump"] += 1;

								}


							}
						}


					}

					// Neplatny radek, nenalezen validni opcode, ani komentar, ani prazdny radek
					if($found == false){
						$err = "Neplatny opcode na radku "; 
						$errLine = $line + 1;
						new Killer(22, "Neplatny opcode na radku ".($line+1));
					}


				}

			}



		}

		private function generateXML(){


			$xml = new SimpleXMLElement("<?xml version='1.0' encoding='UTF-8'?><program></program>");
			$xml->addAttribute('language', 'IPPcode20');
           	
           	$order = 1;

           	foreach ($this->program as $i => $instruction) {
           		$instrXml = $xml->addChild('instruction');
           		$instrXml->addAttribute('order', $instruction->loc);
           		$instrXml->addAttribute('opcode', $instruction->instrType->opcode);

           		for($i = 1; $i <= $instruction->instrType->argc; $i++){
           			$argXml = $instrXml->addChild('arg'.$i, $instruction->argv[$i-1]);

           			$argXml->addAttribute('type', $instruction->argvTypes[$i-1]);
           		}
           		//$instrXml = $xml->addChild('/instruction');
           	 }

			echo $xml->asXML();

		}


	}



 ?>