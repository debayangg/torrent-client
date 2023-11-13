def bencode_encode(value):

    if isinstance(value,bytes):
        return f"{len(value)}:".encode()+value
    elif isinstance(value,str):
        return f"{len(value)}:{value}".encode()
    elif isinstance(value,int):
        return f"i{value}e".encode()
    elif isinstance(value,list):
        return f"l{''.join([bencode_encode(x) for x in value])}e"
    elif isinstance(value,dict):
        res="d".encode()
        for key in value.keys():
            res+=bencode_encode(key)+bencode_encode(value[key])
        res+="e".encode()
        return res

def decode_bencode(bencoded_value):

    decode_bencode.list_current_index=0
    current_index = 0
    # Code for decoding -> string
    # returns a str value
    if chr(bencoded_value[0]).isnumeric():
        first_colon_index = bencoded_value.find(b":")
        length_of_string =int(bencoded_value[:first_colon_index])
        digits=len(str(length_of_string))
        if first_colon_index == -1:
            raise ValueError("Invalid encoded value")
        
        decode_bencode.list_current_index = first_colon_index+1+length_of_string
        return bytes_to_str(bencoded_value[first_colon_index+1:first_colon_index+1+length_of_string])
    
    
    # Code for decoding -> integer
    # returns a integer value
    elif chr(bencoded_value[0]) == "i":
        end_of_int_index = bencoded_value.find(b"e")
        if(end_of_int_index == -1):
            raise ValueError("Invalid encoded value")
        
        decode_bencode.list_current_index = end_of_int_index
        return int_bytes_to_str(bencoded_value[1:end_of_int_index])
    
    # Code for decoding -> list
    # returns a list of values -> [...]
    elif chr(bencoded_value[0]) == "l":
        current_index = 1
        list_of_values = []
    
    # iterate through bencoded_value until 'e' end of the list
    # current_index = first char of the next string/int(value) in the list
    # Updation: current_index = next char of the next string/int in the list or end of list
    # we append the decoded value to the list_of_values
        
        while chr(bencoded_value[current_index]) != "e":
            #print(chr(bencoded_value[current_index])) #<- for debugging
            
            # checks if the current value is a string and decodes it
            
            if(chr(bencoded_value[current_index]).isnumeric()):
                try:
                    list_first_colon_index = bencoded_value.find(b":",current_index)
                    length_of_string = int(bencoded_value[current_index:list_first_colon_index])
                    digits=len(str(length_of_string))
                    #print(length_of_string,digits,current_index,current_index+length_of_string+digits+1)                    
                    value= decode_bencode(bencoded_value[current_index:current_index+length_of_string+digits+1])
                except:
                    raise ValueError("Invalid encoded value")
                current_index = current_index + length_of_string + digits + 1
                list_of_values.append(value)
            
            
            # checks if the current value is an integer and decodes it
            
            elif(chr(bencoded_value[current_index]) == "i"):
                end_of_int_index = bencoded_value.find(b"e",current_index)
                #print(end_of_int_index)
                if(end_of_int_index == -1):
                    raise ValueError("Invalid encoded value")
                value = decode_bencode(bencoded_value[current_index:end_of_int_index+1])
                current_index = end_of_int_index+1
                list_of_values.append(value)

            # checks if the current value is a list and decodes it    
        
            elif(chr(bencoded_value[current_index]) == "l"):
                [value,end_of_list_index] = decode_helper(bencoded_value[current_index:])
                #print(end_of_list_index,value)
                #print(end_of_list_index,chr(bencoded_value[end_of_list_index]))
                current_index = end_of_list_index + current_index
                list_of_values.append(value)
            
            elif((chr(bencoded_value[current_index]) == "d")):
                [value,end_of_list_index] = decode_helper(bencoded_value[current_index:])
                #print(end_of_list_index,value)
                #print(end_of_list_index,chr(bencoded_value[end_of_list_index]))
                current_index = end_of_list_index + current_index

            else:
                raise ValueError("Invalid encoded value")
        decode_bencode.list_current_index = current_index+1    
        return list_of_values
    
    elif chr(bencoded_value[0]) == "d":
        current_index = 1
        list_keys = []
        list_values = []
        isKey = True
        while chr(bencoded_value[current_index]) != "e":
            #print(current_index,bencoded_value[current_index:]) #<- for debugging
            if isKey==True:
                isKey = False
                #print(chr(bencoded_value[current_index])) #<- for debugging
                if(chr(bencoded_value[current_index]).isnumeric()):
                    try:
                        list_first_colon_index = bencoded_value.find(b":",current_index)
                        length_of_string = int(bencoded_value[current_index:list_first_colon_index])
                        digits=len(str(length_of_string))
                        #print(length_of_string,digits,current_index,current_index+length_of_string+digits+1)                    
                        value= decode_bencode(bencoded_value[current_index:current_index+length_of_string+digits+1])
                    except:
                        raise ValueError("Invalid encoded value")
                    current_index = current_index + length_of_string + digits + 1
                    list_keys.append(value)
                
                elif(chr(bencoded_value[current_index]) == "i"):
                    end_of_int_index = bencoded_value.find(b"e",current_index)
                    #print(end_of_int_index)
                    if(end_of_int_index == -1):
                        raise ValueError("Invalid encoded value")
                    value = decode_bencode(bencoded_value[current_index:end_of_int_index+1])
                    current_index = end_of_int_index+1
                    #print(value,list_keys)
                    list_keys.append(int(value))

                else:
                    raise ValueError("Invalid encoded value")
                
            else:
                #print(current_index,bencoded_value[current_index:])
                isKey = True
                [value,end_index]=decode_helper(bencoded_value[current_index:])
                if chr(bencoded_value[current_index]) == "i":
                    current_index = end_index + current_index+1
                else:
                    current_index = end_index + current_index
                #print(list_keys,list_values,value,current_index)
                list_values.append(value)
        
        decode_bencode.list_current_index = current_index+1
        return dict(zip(list_keys,list_values))

    else:
        raise NotImplementedError("Only strings are supported at the moment")

# helper function
# gives callee function access to current_index(final value) in decode_bencode()
def decode_helper(bencoded_value):
    #print(bencoded_value)
    value = decode_bencode(bencoded_value)
    return [value,decode_bencode.list_current_index]

def str_to_int(data):
    if isinstance(data, str):
        return int(data)

def bytes_to_str(data):
    try:
     if isinstance(data, bytes):
        return_value= data.decode()
        '''if return_value[0].isnumeric() or return_value[1:].isnumeric():
            return int(return_value)''' 
        return return_value
    except:
        return data

def int_bytes_to_str(data):
    try:
        if isinstance(data,bytes):
            return int(data.decode())
        else:
            raise Exception
    except:
        return data
