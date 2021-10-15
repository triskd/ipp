<?php 

require_once("Killer.php");

/*
	Trida definujici typ instrukce,
	Trida obsahuje verejne argumenty: 
		$opcode - (unikatni) operacni kod instrukce, 
		$argc - pocet argumentu, 
		$argTypes[] - povolene hodnoty 'label', 'var', 'symb', 'type'
					- typ prvniho argumentu funkce je na indexu 0
	Trida obsahuje verejne metody:
		__contruct(opcode, argc) - vytvari novou instanci Instrype
								 - opcode je operacni kod instrukce
								 - argc pocet argumentu instrukce
		setArgTypes([]) - vytvorene instanci nastavi pole typu argumentu funkce
						- pole typu argumentu funkce 
						- pri zadani pole jehoz delka neodpovida poctu argumentu -> ukonceni s chybovym kodem 99
		copy() - vraci novou instanci InstrType, naplnenou stejnymi daty
*/
class InstrType{

	public $opcode;
	public $argc;
	public $argTypes = [];

	public function __construct($opcode, $argc){

		$this->opcode = $opcode;
		$this->argc = $argc;

	}

	public function setArgTypes($args){


		if($this->argc == 0 && $args == 0){

			return 0;

		}else{

			if($this->argc == sizeof($args)){


				foreach( $args as $argKey => $argType){

					if($argType == "label"){

						array_push($this->argTypes, $argType);

					}else if($argType == "var"){

						array_push($this->argTypes, $argType);


					}else if($argType == "symb"){
						
						array_push($this->argTypes, $argType);

					}else if($argType == "type"){
						
						array_push($this->argTypes, $argType);


					}else{

						new Killer(99, "Vnitrni chyba scriptu\n- vytvareni typu instrukce s neznamym typem argumentu");
					
					}
					
				}

			}else{

				new Killer(99, "Vnitrni chyba scriptu\n- vytvareni typu instrukce s neodpovidajicim poctem typu argumentu");

			}
			
		}
		
	}

	public function copy(){

		$newInstr = new InstrType($this->opcode, $this->argc);
		$newInstr->setArgTypes($this->argTypes);

		return $newInstr;
	}


}

/*
	Trida reprezentuci vyskyt konkretni instrukce ve zdrojovem kodu
*/

class Instruction{

	public $instrType;
	public $txt;
	public $line;
	public $loc;
	public $comm;
	public $argvNotCheck = [];
	public $argv = [];
	public $argvTypes = [];

	public function __construct($instrType, $txt, $line, $loc){

		if($instrType instanceof InstrType){

			$this->instrType = $instrType->copy();
			$this->txt = $txt;
			$this->line = $line;
			$this->loc = $loc;
			$this->comm = false;

		}else{

			new Killer(99, "Instruction.php Instruction __construct()");

		}

	}

	public function argCheck(){

		foreach ($this->instrType->argTypes as $argc => $validArgvType) {

			switch ($validArgvType) {

				case 'label':
					
					if(preg_match("/^([a-z]|[A-Z]|[\_\-\$\&\%\*\!\?])([a-z]|[A-z]|[\_\-\$\&\%\*\!\?]|[0-9])*/", $this->argvNotCheck[$argc], $decodeArg1)){

						array_push( $this->argv,$this->argvNotCheck[$argc]);
						array_push($this->argvTypes, "label");

					}else{

						new Killer(23, "Chybna syntaxe instrukce - ".$this->instrType->opcode." (loc: ".$this->loc."), na radku: ".$this->line."\n   chybny label: ".$this->argvNotCheck[$argc]);

					}

				break;
				
				case 'var':
					
					if(preg_match("/^((GF)|(LF)|(TF))@([a-z]|[A-Z]|[\_\-\$\&\%\*\!\?])([a-z]|[A-z]|[\_\-\$\&\%\*\!\?]|[0-9])*/", $this->argvNotCheck[$argc], $decodeArg1)){

						array_push($this->argv, $this->argvNotCheck[$argc]);
						array_push($this->argvTypes, "var");

					}else{

						new Killer(23, "Chybna syntaxe instrukce - ".$this->instrType->opcode." (loc: ".$this->loc."), na radku: ".$this->line."\n   chybna promenna: ".$this->argvNotCheck[$argc]);

					}

				break;

				case 'symb':

					// var_dump($this);
					//arg1 je promenna
					if(preg_match("/^((GF)|(LF)|(TF))@([a-z]|[A-Z]|[\_\-\$\&\%\*\!\?])([a-z]|[A-z]|[\_\-\$\&\%\*\!\?]|[0-9])*$/",$this->argvNotCheck[$argc], $decodeArg1)){

						array_push($this->argv, $this->argvNotCheck[$argc]);
						array_push($this->argvTypes, "var");


					//arg1 je konstanta int
					}else if(preg_match("/^int@((\+|\-)?((0){1}|([1-9][0-9]*))$)/", $this->argvNotCheck[$argc], $decodeArg1)){

						array_push($this->argv, $decodeArg1[1]);
						array_push($this->argvTypes, "int");

					//arg1 je konstanta bool
					}else if(preg_match("/^bool@((true)|(false))$/", $this->argvNotCheck[$argc], $decodeArg1)){
						
						array_push($this->argv, $decodeArg1[1]);
						array_push($this->argvTypes, "bool");
					
					//arg1 je konstanta string
						//^(string)@((((\\[0-9]{3})|([0-9]+)|[^\s#]+))+)?$
					}else if(preg_match('/^(string)@((([^\\\])|(\\\[0-9]{3})|([0-9])|([^\s\\\#])((\\[0-9]{3})|([0-9]+)|[^\s\\\#]+))+)?$/', $this->argvNotCheck[$argc], $decodeArg1)){

						if(sizeof($decodeArg1) >= 3){
							array_push($this->argv, $decodeArg1[2]);
						}else{
							array_push($this->argv, "");
						}

						array_push($this->argvTypes, "string");

					//arg1 je konstata nil
					}else if(preg_match("/^nil@nil$/", $this->argvNotCheck[$argc], $decodeArg1)){

						array_push($this->argv, "nil");
						array_push($this->argvTypes, "nil");

					}else{
						
						new Killer(23, "Chybna syntaxe instrukce - ".$this->instrType->opcode." (loc: ".$this->loc."), na radku: ".$this->line."\n   chybna promenna nebo konstanta: ".$this->argvNotCheck[$argc]);

					}
				
				break;

				case 'type': 
					
					if(preg_match("/^(string)|(int)|(bool)$/", $this->argvNotCheck[$argc], $decodeArg1)){
					
						array_push($this->argv, $decodeArg1[0]);
						array_push($this->argvTypes, "type");
					
					}else{

						new Killer(23, "Chybna syntaxe instrukce - ".$this->instrType->opcode." (loc: ".$this->loc."), na radku: ".$this->line."\n   chybna promenna nebo konstanta: ".$this->argvNotCheck[$argc]);

					}
				
				break;
			}


		}


	}


}

interface InstrInterface{

	public function decode();
	public function analyze();

}


class Instr0Arg extends Instruction implements InstrInterface{


	public function decode(){

		$valid = false;
		
		if(preg_match("/^\s*(".$this->instrType->opcode.")\s*(\s*(#)+.*)?$/i", $this->txt, $matches)){

			$valid = true;

			$this->argvNotCheck = [];

		 	if(sizeof($matches) >= 3){
		 		

		 		if($matches[3] == "#"){

		 			$this->comm = true; // na radku je spolecne s instrukci komentar;
		 		}
		 	
		 	}

		}

		if($valid == false){

			new Killer(23, "Chybna syntaxe instrukce - ".$this->instrType->opcode." (loc: ".$this->loc."), na radku: ".$this->line);

		}

		// var_dump($this);


	}


	// public function argCheck(){

	// }


	public function analyze(){
		$this->decode();
	}


}

class Instr1Arg extends Instruction implements InstrInterface{



	public function decode(){


		//vstupni radek instrukce ma tvar opcode arg1 (#kosdkosd)		
		if(preg_match("/^\s*(".$this->instrType->opcode.")\s+(\S+)(\s*(#)+.*)?$/i", $this->txt, $matches)){



			if(sizeof($matches) >= 2){
				array_push($this->argvNotCheck, $matches[2]);
			}

			if(sizeof($matches) >= 4){

				if($matches[4] == '#'){
					$this->comm = true;
				}

			}

		//	var_dump($this);


		}else{

			new Killer(23, "Chybna syntaxe instrukce - ".$this->instrType->opcode." (loc: ".$this->loc."), na radku: ".$this->line."\n   neocekavany pocet argumentu");

		}
	
	}


	// public function argCheck(){

	// }

	public function analyze(){
		$this->decode();
		$this->argCheck();
	}

	




}

class Instr2Arg extends Instruction implements InstrInterface{



	public function decode(){

		if(preg_match("/^\s*(".$this->instrType->opcode.")\s+(\S+)\s+(\S+)(\s*(#)+.*)?$/i", $this->txt, $matches)){

			if(sizeof($matches) >= 3){

				array_push($this->argvNotCheck, $matches[2]);
				array_push($this->argvNotCheck, $matches[3]);
				
			}
			
			if(sizeof($matches) >= 5){
				
				if($matches[5] == '#'){
					$this->comm = true;
				}

			}



		}else{

			new Killer(23, "Chybna syntaxe instrukce - ".$this->instrType->opcode." (loc: ".$this->loc."), na radku: ".$this->line."\n   neocekavany pocet argumentu");

		}
		
	
	}


	// public function argCheck(){

	// }

	public function analyze(){
		$this->decode();
		$this->argCheck();
	}

	



}

class Instr3Arg extends Instruction implements InstrInterface{



	public function decode(){

		if(preg_match("/^\s*(".$this->instrType->opcode.")\s+(\S+)\s+(\S+)\s+(\S+)(\s*(#)+.*)?$/i", $this->txt, $matches)){

			if(sizeof($matches)  >= 4){
				array_push($this->argvNotCheck, $matches[2]);
				array_push($this->argvNotCheck, $matches[3]);
				array_push($this->argvNotCheck, $matches[4]);
			}

			if(sizeof($matches) >= 6){
				if($matches[6] == '#'){
					$this->comm = true;
				}	
			}

			// var_dump($matches);

		}else{

			new Killer(23, "Chybna syntaxe instrukce - ".$this->instrType->opcode." (loc: ".$this->loc."), na radku: ".$this->line."\n   neocekavany pocet argumentu");

		}
		
	
	}


	// public function argCheck(){

	// }


	public function analyze(){
		$this->decode();
		$this->argCheck();
	}


}


?>