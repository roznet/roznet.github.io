---
layout: post
title:  "Efficient Parsing for Fit files"
date:   2018-12-20 18:02:13 +0100
categories: "Data"
comments: true
---

[So I got to the point I wanted to speed up the parsing of Fit Files]({% post_url 2018-12-15-data-science-for-fitness %})

# Fast Swift Parsing of Fit Files

The standard fit sdk in c++ was out because of speed, I started to work out how the c version was working to see how to link that into swift.

There are two main files of interest in the [c examples](https://github.com/roznet/fit-sdk-swift/tree/master/RZFitFile/sdk) of the standard [Fit SDK](https://www.thisisant.com/resources/fit): 

* `fit_convert.c` where the actual logic of the parsing is implemented
* `fit_example.h` where you can find the definitions of the different fields

I found the implementation of the parsing logic quite fascinating. It runs via a loop that maintain a state and is very robust to re-entry and processing arbitrary (small) buffer size. Clearly, this was implemented with keeping the memory tight in mind. You need to call the function `FitConvert_Read` and feed it more data in a buffer while the return value is `FIT_CONVERT_CONTINUE` or process a message when the return value is `FIT_CONVERT_MESSAGE_AVAILABLE`.

# C pointers and swift

The first challenge was to figure out the swift syntax to call and interact with the c function. It turns out swift has a very neat way of [interacting with pointers](https://developer.apple.com/documentation/swift/swift_standard_library/manual_memory_management). 

First you need to pass in a `FIT_UINT8 *` with the address to read the Fit Data from. In swift, from the `Data` object you can then access the equivalent `UnsafePointer<UInt8>` and pass it to the c function using `withUnsafeByes`:

```swift
       while convert_return == FIT_CONVERT_CONTINUE {
            data.withUnsafeBytes({ (ptr: UnsafePointer<UInt8>) in
                repeat {
                    convert_return = FitConvert_Read(&state, ptr, FIT_UINT32(data.count))
 
```

The next challenge is when a message is received, you need to typecase the pointer to a pointer the appropriate structure to extract the information. For example, for a `struct FIT_RECORD_MESG*`, in c you would convert the pointer to `(FIT_RECORD_MESG*)ptr`. In swift you can achieve the same using `withMemoryRebound(to:, capacity:)` as follows:

```swift
func conv( uptr : UnsafePointer<UInt8>){
	uptr.withMemoryRebound(to: FIT_RECORD_MESG.self, capacity: 1) {
		callfunc( ptr: $0 )
	}
}
```

You can see the final swift code calling and processing the convert function [here](https://github.com/roznet/fit-sdk-swift/blob/master/RZFitFile/src/RZFitFile.swift)

# Processing the types definitions in Fit Files

The next challenge was that all the conceptual definition of the types in the fit files are either `typedef` of numbers or c structures. And there is almost 8000 lines of such definition in the c header files. I wanted to be able to convert the files from these structures and integer code into a more processing friend key value representation of strings to double.

For this I decided to convert the almost 8000 lines of c typedefs into a corresponding swift file of definition. Given that the SDK and fields are regularly updated it was out of the question to process even semi-manually with regex... So I wrote a [python script](https://github.com/roznet/fit-sdk-swift/blob/master/RZFitFile/fitconv.py) that would convert the c code to swift...

There are three main type of code I had to convert, enum typedef which I would convert to function mapping the integer code to a string. A good example would be

```c
typedef FIT_ENUM FIT_GENDER;
#define FIT_GENDER_INVALID                                                       FIT_ENUM_INVALID
#define FIT_GENDER_FEMALE                                                        ((FIT_GENDER)0)
#define FIT_GENDER_MALE                                                          ((FIT_GENDER)1)
#define FIT_GENDER_COUNT                                                         2
```

that the python code would convert to:

```swift
func rzfit_gender_string(input : FIT_ENUM) -> String? 
{
  switch  input {
    case FIT_GENDER_FEMALE: return "female";
    case FIT_GENDER_MALE: return "male";
    default: return nil
  }
}
```

The python code is quite straight forward and generate the string by removing the type name and going lower case...


```c
typedef struct
{
   FIT_STRING name[FIT_SPEED_ZONE_MESG_NAME_COUNT]; //
   FIT_MESSAGE_INDEX message_index; //
   FIT_UINT16 high_value; // 1000 * m/s + 0,
} FIT_SPEED_ZONE_MESG;
```

That would have to be converted to a function to convert the values `high_value` and a function to convert the enums `FIT_MESSAGE_INDEX`:

```swift
func rzfit_speed_zone_mesg_value_dict( ptr : UnsafePointer<FIT_SPEED_ZONE_MESG>) -> [String:Double] {
  var rv : [String:Double] = [:]
  let x : FIT_SPEED_ZONE_MESG = ptr.pointee
  if x.high_value != FIT_UINT16_INVALID  {
    let val : Double = (Double(x.high_value))/Double(1000)
    rv[ "high_value" ] = val
  }
  return rv
}
func rzfit_speed_zone_mesg_enum_dict( ptr : UnsafePointer<FIT_SPEED_ZONE_MESG>) -> [String:String] {
  var rv : [String:String] = [:]
  let x : FIT_SPEED_ZONE_MESG = ptr.pointee
  if( x.message_index != FIT_MESSAGE_INDEX_INVALID ) {
    rv[ "message_index" ] = rzfit_message_index_string(input: x.message_index)
  }
  return rv
}
```

# Putting it all together

Equipped with all these 9000 lines of auto generated functions to convert the c struct into swift dictionaries, all what remained was to put it all together. A message read from a fit file contains a message number as `FIT_MESG_NUM` c type, which just required now a big auto generated switch putting the result of the correct function into a swift class container as below:

```swift
func rzfit_build_mesg(num : FIT_MESG_NUM, uptr : UnsafePointer<UInt8>) -> RZFitMessage?{
    var rv : RZFitMessage? = nil
    switch num {
  case FIT_MESG_NUM_FILE_ID:
    uptr.withMemoryRebound(to: FIT_FILE_ID_MESG.self, capacity: 1) {
      rv = RZFitMessage( mesg_num:    FIT_MESG_NUM_FILE_ID,
                         mesg_values: rzfit_file_id_mesg_value_dict(ptr: $0),
                         mesg_enums:  rzfit_file_id_mesg_enum_dict(ptr: $0))
    }
  case FIT_MESG_NUM_CAPABILITIES:
    uptr.withMemoryRebound(to: FIT_CAPABILITIES_MESG.self, capacity: 1) {
      rv = RZFitMessage( mesg_num:    FIT_MESG_NUM_CAPABILITIES,
                         mesg_values: rzfit_capabilities_mesg_value_dict(ptr: $0),
                         mesg_enums:  rzfit_capabilities_mesg_enum_dict(ptr: $0))
    }
 //...
```

The [project](https://github.com/roznet/fit-sdk-swift) contains a small command line utility and a sample file, and it parses in 0.044 second 6718 messages:

```
Parsing /Users/brice/Development/public/fit-sdk-swift/samples/running.fit
6718 messages in 0.04484999179840088 seconds
Program ended with exit code: 0
```

As a comparison the c++ parsing code from the original sdk would parse the same file in 3.88 seconds

```
FIT Decode Example Application
Decoded FIT file /Users/brice/Development/public/fit-sdk-swift/samples/running.fit in 3.884835.
Program ended with exit code: 0
```
