# What?

Tagi is a contextual tagging engine. You can use it to tag files with extra metadata and it can then generate links to other tagged files based off the contents of the files themselves.

# Why?

I use a personal wiki to write fiction. This has a lot of benefits, for example when a character gets an item you can easily update their character page by clicking on their name. Or maybe you just want to know what monsters are in a location, you can easily search for them based on habitat.

However, I was getting tired of typing out the full url to a page. Typing out "\[\[Setting/Fauna/Dragon\]\[dragon\]\]" is tiring when all I wanted to type out was "dragon".

So I decided to create a wiki that would do all that tedious work for me. 

# How?

At it's core, tagi is a tagging engine. You can tag any file with arbitrary tags. After tagging a file, you can search for it by its tags.

Tagi though, has a concept of two tag types. Linking tags and context tags.

A linking tag is a tag that can be used to link to a document. It can be a character's name, nickname, or whatever. The only important characteristic is that you want that particular word to link to the document.

The magic comes from the context tags. These tags will typically be more numerous than linking tags and are used to pick the most appropriate document when using a linking tag. When searching for a link, the document that has the most context tags in common with the current document will be used for that link.

This allows you to have multiple pages that can be linked with the one word, but depending on where you link it, different pages can be chosen.

# Show me

Imagine you are writing your magnum opus. A real tearjerker (with laugh at loud moments) quadrilogy about a rising star in a down on its luck marine corp. A story about a monkey in the marines who just wants to be the best that she can be.

You start off by writing her character page. Dutifully you write down that she likes bananas, hates liars, but is a little bit naive. You save it in the aptly named file: monkey.txt 

Armed with this file, you set out to categorise it in your soon to be magnificent database

	tagi tag monkey.txt Monkey animal female character marine
	
You look at monkey.txt for a few minutes, proud that you had so accurately categorised your prised primate character. Suddenly an inspiration strikes you. What if it was a space opera! Feverishly you add that Monkey joined the space marines, topping it off with a new tag.

	tagi tag monkey.txt space-marine

Then you think to yourself, "Wait. The space marines and the standard marines don't like each other. Monkey can't belong to both!" The only thing you can do (after mentioning that in marines.txt) is to remove the marine tag from Monkey's page.

	tagi remove-tag monkey.txt marine

Perfect. Satisfied with the knowledge that no one could now confuse Monkey's allegiance, you knuckle down and start the hard work of creating a universe and a plot, generating many delicately intertwined pages. A master pieces of documents linking to other documents. You look at it suspiciously. It may be too much of a masterpiece.

You decide to check Monkey's page

	tagi links-to monkey.txt

Lo and behold too many pages were linking to Monkey. Most of the links where of words that shouldn't go to Monkey's page. You realise that most of those words weren't directly about Monkey, but actually described the heroic primate herself. 

You reassign them as into Monkey's context

	tagi tag monkey.txt --context space-marine animal female character

Fixed. Now animal wouldn't always mean Monkey. Things made sense again.

You reach a critical point in the novel. Somehow Monkey needs to fix the relationship between the space marines and Civilian Entertainment Corporation. But how?

Despairing you look for any possible relationships Monkey could use.

	tagi links-from monkey.txt

You see that not only does Monkey have ties to the space marines, but she also owns a TV made by the Civilian Entertainment Corporation. "Perfect!" You exclaim, knowing exactly. what to do.

Many more words in and your novel starts look like a serious contender. You have a real heavyweight in the realm of speculative socio-political fiction. This was no time to pat yourself on the back though. You needed a villain from the planet of Zorgax IV. Luckily you knew you had already had extensive documentation on the situation in the Zorgax system.

All that untapped potential just waiting for someone to tap it. You tap it.

	tagi search ZorgaxIV villain

The sordid history of Zorgax unfolds before your eyes. You spy a name among the list, Hellbeam. The scummiest of scummy scum that ever scum craweled out of the scum filled sewers of Zorgax IV. Just the sort of lowlife you were looking for.
	
As you progress through the heart-wrenching betrayal by Monkey's closest friend, a whim strikes you. You run a command you had heard about from the dark underworld that is **The Internet**.

	tagi linkify monkey.txt
	
Your screen fills up with the locations of every link to another document found in your characters document. You have no idea how to use it. You guess it could be useful. Why did you run this command again? Uncertain, you get back to the serious business of writing. Running strange commands from the internet was a silly idea anyway. 

After sweating blood and tears, you near the end of your novel. Quickly you add some major character development. Monkey loses an eye. Tears freely run from your own eyes as Monkey saves her rival from certain death, getting partially blinded in the process. Her squad-mates honour that sacrifice with a new name, Bullseye, after her new competence at aiming.

You add it as another linking tag

	tagi tag monkey.txt Bullseye

Now every time some calls Monkey Bullseye, you are confident it will link to Monkey.

However, when you finish the novel, you realise that having less eyes doesn't actually reduce visual interference, but actually makes it harder to aim. Biology sure is a tricky thing.

There is only one way to fix this. You need to give Monkey a different name. You settle on the much less sinister name Cyclops.

	tagi relink monkey.txt Bullseye Cyclops

All the references to Bullseye have now become the more appropriate name Cyclops. Book finished!

You give yourself a week to bask in the glory of finishing one fantastic, prize winning, perfect novel. Three to go. Rolling up your sleeves, you get to work on the next even more perfect novel. Future generations will study your quadrilogy as a piece of important history that sparked the social revolution that made their current utopia possible. You couldn't have done this without an excellent categorising system.

# License

MIT
