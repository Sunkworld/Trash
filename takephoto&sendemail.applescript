try
	tell application "Photo Booth"
		activate
	end tell
	do shell script "touch /Users/Yuuko/Pictures/Photo\\ Booth\\ Library/Pictures/skfjsa.jpg"
	do shell script "rm /Users/Yuuko/Pictures/Photo\\ Booth\\ Library/Pictures/*"
	tell application "System Events"
		tell process "Photo Booth"
			delay 2
			key code 36 using {option down, command down}
		end tell
	end tell
	
	delay 2
	tell application "Photo Booth" to quit
	
	do shell script "touch /Users/Yuuko/Desktop/slfjaskdf.jpg"
	do shell script "rm /Users/Yuuko/Desktop/*.jpg"
	do shell script "mv /Users/Yuuko/Pictures/Photo\\ Booth\\ Library/Pictures/* /Users/Yuuko/Desktop"
	do shell script "mv /Users/Yuuko/Desktop/*.jpg /Users/Yuuko/Desktop/1.jpg"
	
	tell application "Airmail 2"
		activate
		set theMessage to make new outgoing message with properties {subject:"the subject", content:"the content"}
		tell theMessage
			set sender to "365062829@qq.com"
			set signature to "My signature"
			make new to recipient at end of to recipients with properties {name:"yuuko_vps", address:"yuuko_vps@126.com"}
			make new mail attachment with properties {filename:"Users:Yuuko:Desktop:1.jpg" as alias}
			sendmessage
		end tell
	end tell
on error
	do shell script "/System/Library/CoreServices/Menu\\ Extras/User.menu/Contents/Resources/CGSession -suspend"
end try