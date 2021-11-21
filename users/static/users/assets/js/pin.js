/* 
# Let's start
const MyPin = new pin(element, {quantity: 4, type: 'password'}); 

# Options
quantity - number - number of inputs (default: 4)
placeholder - string - allows to change placeholder character (default: '-')
type - string - (default: 'number')
onEnd - function - 

# Methods
value - returns value of all inputs 
e.g MyPin.value

disable / enable - changes the disabled state
e.g MyPin.disable();

focus(inputIndex) - focus selected input
e.g MyPin.focus(2);

blur() - focus out for all inputs
e.g MyPin.blur();

clear
e.g MyPin.clear();

set - allows you to set the value of a pin input
e.g MyPin.set(3213); or MyPin.set('3', 2);

# States
disabled - boolean (true/false)
ended - boolean (true/false)
touched - boolean (true/false)

*/

class pin {
	constructor(parent, options) {
		const defaultOptions = {
			quantity: 7,
			placeholder: '-',
			type: 'string',
			onEnd: null,
		};
		this.plugin = 'PIN PLUGIN';
		this.parent = parent;
		this.inputs = [];
		this.state = {
      disabled: false,
			ended: false,
			touched: false,
    };
		this.options = Object.assign({}, defaultOptions, options);
		this.render();
	}

	build(i) {
		const inputs = this.inputs,
					input = document.createElement("input");

		input.className = "pin-input";
		input.dataset.id = i;
		input.autocomplete = "off";
		input.type = this.options.type;
		input.placeholder = this.options.placeholder;
		input.setAttribute("aria-label", "Pin input");
		input.setAttribute("maxlength", 1);
		inputs.push({ id: i, element: input, value: input.value});
		return this.events(input);
	}
	
	onEvent() {
		let is_function_onEnd = typeof this.options.onEnd === 'function',
				is_pin_ended = this.value.length == this.options.quantity;
			
		// Update state 'ended'
		this.state.ended = is_pin_ended && !this.state.ended ? true : false;
		if (is_function_onEnd) {
			if (is_pin_ended) this.options.onEnd();
		} else throw new Error(this.plugin + ' --> onEnd parametr is not a function');
		
		// Update value in object
    this.inputs.forEach(input => input.value = input.element.value);
  }

	events(element) {
		let 
			app = this,
			currID = parseInt(element.dataset.id),
			nextID = currID + 1 >= app.options.quantity ? 0 : currID + 1,
			prevID = currID - 1 < 0 ? app.options.quantity - 1 : currID - 1,
			currElement = element;

		element.onclick = event => {
			app.state.touched = true;
			element.select();
		};
	
		element.onkeypress = event => {
			if(element.value.length == 1) element.value = element.value.substring(1);
			if (!/[0-9]/.test(event.key)) event.preventDefault();
		};

		element.onkeyup = event => {
			let keyID = event.keyCode;

			let 
				currElement = app.inputs.find(x => x.id === currID).element,
				prevElement = app.inputs.find(x => x.id === prevID).element,
				nextElement = app.inputs.find(x => x.id === nextID).element;

			let 
				arrowLeftActive = keyID == 37 ? true : false,
				arrowRightActive = keyID == 39 ? true : false,
				backspaceActive = keyID != 8 && keyID != 46 ? true : false,
				isNextID = nextID !== 0 ? true : false,
				isPrevID = prevID !== app.options.quantity - 1 ? true : false,
				isInputHasValue = currElement.value != "" ? true : false;
			
			// Check is the input has only one character
			(element.value + '').length > 1 && (element.value = element.value.slice(-1));
		
			// Go right
			if (backspaceActive && isNextID && !app.state.disabled) {
				if (isInputHasValue) {
					app.state.touched = true;
					nextElement.select();
					nextElement.focus();
				} 
			}
		
			// Go left
			if (!backspaceActive && isPrevID && !app.state.disabled) {
				app.state.touched = true;
				prevElement.select();
				prevElement.focus();
			}
			
			app.onEvent();
		};

		return element;
	}
	
	set(numbers, inputIndex = null) {
		let error = 0,
				numbersAsString = numbers + '';
		
		if (inputIndex) {
			if (numbers.length+'' == 1) {
				this.inputs[inputIndex].element.value = numbers;
			} else error++;
		} else {
			for (let i = 0; i < numbersAsString.length; i++) {
				if (this.inputs.length >= numbersAsString.length) 
					this.inputs[i].element.value = numbersAsString.charAt(i);
				else
					error++;
			}
		}
		
		if (error != 0) throw new Error(this.plugin + ' --> The entered pin number exceeds the number of inputs');
	}
	
	disable() {
    this.state.disabled = true;
    this.inputs.forEach(o => o.element.disabled = 'disabled');
  }

  enable() {
    this.state.disabled = false;
    this.inputs.forEach(o => o.element.removeAttribute('disabled'));
  }
	
	blur() {
		this.inputs.forEach( o=> o.element.blur() );
	}
	
	focus(index = 0) {
		this.inputs[index].element.focus();
	}
	
	clear() {
		this.inputs.forEach(o => o.element.value = '');
	}
	
	get value() {
		let string = "";
		this.inputs.forEach(o => {
			if ((o.element.value + "").length != 1) 
				string += o.element.value + ""; 
			else
				string += (o.element.value + "").slice(-1);
		});
		return string;
	}

	render() {
		this.parent.innerHTML = '';
		for (let i = 0; i < this.options.quantity; i++) {
			this.parent.appendChild(this.build(i));
		}
	}
}

/*
                |
                |
                |
                |
                V
*/

const MyPin = new pin(document.body.querySelector(".pin-component"), {
	quantity: 7, 
	placeholder: '-',
	type: 'string',
	onEnd: () => { 
		let team = MyPin.value.replace(/^0+/, '')
		document.getElementById('team_num_reg').value = team },
	//onEnd: ()=>{MyPin.value}
});



// TEST
function getMessage(index) {
	let message = '00000'.split('');
	var result = '';
	
	index > MyPin.options.quantity && (index = index%(MyPin.options.quantity));
	for(let i=0; i< MyPin.options.quantity; i++) {
		let n = index+i;
		n >= message.length && (n=n%MyPin.options.quantity);
		result += message[n];
	}
	return result;
}
let x = 0;
let testInterval = setInterval(()=>{
	if (MyPin.state.touched) {
		MyPin.clear();
		clearInterval(testInterval);
	} else {
		x++;
		x >= MyPin.options.quantity && (x=0);
		MyPin.set(getMessage(x));
		onEnd = ()=>{  fillData(MyPin.value)	}
	}
}, 100);