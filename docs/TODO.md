# UMA MUSUME (UmaPlay) – Backlog (organized)

This organizes the mixed notes into a clear, actionable backlog. Items are grouped by workstream and priority. “Later” holds non-urgent ideas. 

================================================================================

## 0.4

### 0.4.1

Dummiez
opened 4 days ago
I can't seem to get the adb mode to identify the devices (using LDPlayer), I've also tried Bluestacks which appears on the adb list as well with the same issue. The adb device naming is also a bit confusing to me, does it want the network port or the device name like emulator-5555? (as it appears when using adb devices)

C:\LDPlayer\LDPlayer9>adb devices -l
List of devices attached
emulator-5555          device product:SM-S9210 model:SM_S9210 device:star2qltechn transport_id:1

C:\LDPlayer\LDPlayer9>adb connect localhost:5555
connected to localhost:5555

C:\LDPlayer\LDPlayer9>adb devices -l
List of devices attached
emulator-5555          device product:SM-S9210 model:SM_S9210 device:star2qltechn transport_id:1
localhost:5555         device product:SM-S9210 model:SM_S9210 device:star2qltechn transport_id:3


DominicS48
opened 3 days ago
So I'm trying to run the bot for fan runs during which I never want it to use an alarm clock. I disabled the option for "Try again on failed goal", however the tooltip makes me unsure if this is the proper use of this button. Either way, after failing a goal race, the bot will select Try Again, thus uising an alarm clock. However on the following screen which contains the button for View Results and Race, as well as the alarm clock symbol in the top left, the bot will hang and eventually stop.

22:35:23 INFO    race.py:1022: [race] Clicked green 'Race' button (popup) confirmation
22:35:23 INFO    race.py:1031: Waiting for race lobby to appear
22:35:32 DEBUG   race.py:641: [race] View Results active probability: 1.000
22:35:38 DEBUG   race.py:788: [race] Looking for button_green 'Next' button. Shown after race.
22:35:40 DEBUG   race.py:801: [race] Looking for race_after_next special button. When Pyramid
22:35:44 DEBUG   yolo_local.py:108: saved low-conf training debug -> C:\Users\Domin\Umaplay\debug\ura\general\raw\general_20251115-223544_735_ui_mood_0.69.png
22:35:45 DEBUG   yolo_local.py:108: saved low-conf training debug -> C:\Users\Domin\Umaplay\debug\ura\general\raw\general_20251115-223545_894_ui_mood_0.68.png
22:35:47 DEBUG   yolo_local.py:108: saved low-conf training debug -> C:\Users\Domin\Umaplay\debug\ura\general\raw\general_20251115-223547_046_ui_mood_0.68.png
22:35:49 DEBUG   yolo_local.py:108: saved low-conf training debug -> C:\Users\Domin\Umaplay\debug\ura\general\raw\general_20251115-223549_317_ui_mood_0.69.png
22:35:49 DEBUG   waiter.py:205: [waiter] timeout after 8.00s (tag=race_after)
22:35:49 INFO    race.py:824: [race] RaceDay flow finished.
22:35:52 DEBUG   yolo_local.py:108: saved low-conf training debug -> C:\Users\Domin\Umaplay\debug\ura\general\raw\general_20251115-223552_144_ui_mood_0.70.png
22:35:55 DEBUG   yolo_local.py:108: saved low-conf training debug -> C:\Users\Domin\Umaplay\debug\ura\general\raw\general_20251115-223555_503_ui_mood_0.69.png
22:36:09 DEBUG   yolo_local.py:108: saved low-conf training debug -> C:\Users\Domin\Umaplay\debug\ura\general\raw\general_20251115-223609_335_ui_mood_0.69.png
22:36:12 DEBUG   yolo_local.py:108: saved low-conf training debug -> C:\Users\Domin\Umaplay\debug\ura\general\raw\general_20251115-223612_172_ui_mood_0.61.png
22:36:19 DEBUG   yolo_local.py:108: saved low-conf training debug -> C:\Users\Domin\Umaplay\debug\ura\general\raw\general_20251115-223619_394_ui_mood_0.71.png
22:36:23 DEBUG   yolo_local.py:108: saved low-conf training debug -> C:\Users\Domin\Umaplay\debug\ura\general\raw\general_20251115-223623_826_ui_mood_0.69.png
22:36:26 DEBUG   yolo_local.py:108: saved low-conf training debug -> C:\Users\Domin\Umaplay\debug\ura\general\raw\general_20251115-223626_162_button_change_0.71.png
22:36:28 DEBUG   yolo_local.py:108: saved low-conf training debug -> C:\Users\Domin\Umaplay\debug\ura\general\raw\general_20251115-223627_982_ui_mood_0.71.png
22:36:29 DEBUG   yolo_local.py:108: saved low-conf training debug -> C:\Users\Domin\Umaplay\debug\ura\general\raw\general_20251115-223629_143_ui_mood_0.68.png
22:36:36 DEBUG   yolo_local.py:108: saved low-conf training debug -> C:\Users\Domin\Umaplay\debug\ura\general\raw\general_20251115-223636_072_ui_mood_0.68.png
22:36:43 DEBUG   yolo_local.py:108: saved low-conf training debug -> C:\Users\Domin\Umaplay\debug\ura\general\raw\general_20251115-223643_485_ui_mood_0.67.png
22:36:47 DEBUG   yolo_local.py:108: saved low-conf training debug -> C:\Users\Domin\Umaplay\debug\ura\general\raw\general_20251115-223646_929_ui_mood_0.60.png
22:36:48 DEBUG   yolo_local.py:108: saved low-conf training debug -> C:\Users\Domin\Umaplay\debug\ura\general\raw\general_20251115-223648_115_ui_mood_0.69.png
22:36:50 DEBUG   yolo_local.py:108: saved low-conf training debug -> C:\Users\Domin\Umaplay\debug\ura\general\raw\general_20251115-223650_480_ui_mood_0.69.png
22:36:54 DEBUG   yolo_local.py:108: saved low-conf training debug -> C:\Users\Domin\Umaplay\debug\ura\general\raw\general_20251115-223653_938_ui_mood_0.71.png
22:36:57 WARNING agent.py:176: Stopping the algorithm just for safeness, nothing happened in 20 iterations
22:36:57 INFO    main.py:354: [BOT] Stopped.

boshido
opened 3 days ago · edited by boshido
Version: 0.4.0
after merge request #73 applied

My Environment Setup

ADB by using usb
SCRCPY - Google Pixel 2 XL
scrcpy --max-fps 10 -b 2M --video-codec=h264 --no-audio
Sepearate YOLO/OCR api run in Linux (Python 3.10, CUDA 13.0 update 2)
uvicorn server.main_inference:app --reload --host 0.0.0.0 --port 8001
Windows 11 VM (Python 3.12)



Weir error check thread, air grove: @

add a togle to 'prefer priority stats if are 0.75 less or equal' disabled by default

also look for 'alone' hints / spirits, we may have a support card below. If not recognized a support_card


@Rosetta:Final tip, only do optional races if:
Never do optional races just because it doesn't look like there's anything else good. Discourage this option in Unity cup web ui


+1 for wit (we want to avoid resting as much as possible), but don't explode blue here

General:
- Create discord roles

BUG:
Rosetta — 8:40

After the bot checks for skills after a hint, it doesn't seem to be able to detect any info on the screen and will always rest regardless of energy value

Claw Machine:
- @Rosetta: Re-check of the logic so it always Win. If first detected plushie is good enough and it is not at the border take it, if not do a full scan. Check the zips on discord.

we have 'silent' yolo detection errors. for example with support_bar, it has 0.31 so it was filtered out before our debug saver
add a check like 'if support type, then you must have support bar, otherwise try again with less confidence

Fast mode bugs:
- Solve

reprocess all events data and trainee data

Handle a new screen class 'Race Stale' to detect the 'advance / next' button and press it 


- @Rosetta:
For Tazuna I have stats > hints for energy overcap priority, but it will still reject dating if energy is high enough even though accepting provides stats and rejecting only a hint (I want energy overcap prevention for her third date)
"""
Author notes: I think this is a bug. This is a problem that should not be happening this way. So we need to investigate what's going on and what this person is trying to to do. This is regarding the energy cap prevention, well, the overflow of energy prevention that we are rotating the options here. But I think it's also related to not only to PALs, but this is also related to in general, because maybe we have this bug also for other support cards, not only for Tasu Nakashimoto or, well, PAL support. Maybe we have this for other ones.
"""


new cards


#### README.md:
- suggest just open terminal as admin in the worst case
- slice the readme to make easier to read
- Update images


Done: Adjusted risk for URA, was overcalculating dynamic risk


Luisao

 — 14/11/2025 0:06
to anyone wondering, the 0.4.0 version is working on MuMuPlayer through the localhost:5557 instead of the default localhost:5555, awesome new feature 😄

NhuNTD

 — 14/11/2025 2:22
do you know how to connect to ldplayer
Luisao

 — 14/11/2025 2:36
u need to discover the default port for this emulator, and edit in your bot

adb
vestovia — 14/11/2025 6:22
change to 127.0.0.1:16384

Saddah

 — 14/11/2025 12:51
where do i get adb install from
actually found it in a scrpy install i did previously
just moved it and it works now


Saddah

 — 16/11/2025 15:03
does ADB mode need a certain resolution on the emulator to work correctly?


Only

 — 14:07
hmm I do get a lot of [skills] skipping 'Medium Straightaways ◎' grade='◎' (already purchased) when it is still ○ [1/2] 


Unknown

 — 1:51
Okay, new suggestion: If the run is at the URA Finale, it should not rest at least at the final turn before the finals



Open Command Prompt and navigate to the Umaplay folder -> installation not clear enough

### 0.4.2

Events:
- how should i respond still fails (chain). Check and validate
- When no event detected, generate a special log in debug folder if 'debug' bool is enabled: gent.py:292: [Event] EventDecision(matched_key=None, matched_key_step=None, pick_option=1, clicked_box=(182.39614868164062, 404.23193359375, 563.8184204101562, 458.83447265625), debug={'current_energy': 64, 'max_energy_cap': 100, 'chain_step_hint': None, 'num_choices': 2, 'has_event_card': False, 'ocr_title': '', 'ocr_description': ''}). 

Bug:
- race.py 867 when getting the style_btns chosen, error of list index out of range


Roseta: Also I don't have a log for it but if it's on fast mode and finds a good training that's capped, it'll return NOOP before checking other trianings and keep looping like that 

Bot Strategy:
One more little idea I've just had - it would be cool if the settings "allow racing over low training" could be expanded into deciding what grades of races this is allowed to trigger with (eg. only G1s)
MagodyBoy — 17:20
and the minimum energy to trigger race, I think right now I check if we have >= 70% of energy

Quality Assurance:
- Color unit testing: detected as yellow the 'green' one "yellow: +0.00"



PhantomDice —> Thanks for supporting project


with f8 also detect the shop

@Unknown

 — 3/11/2025 1:00
Found another "bug" where it stops at Ura races
Stuff I used

thread of 'Unknown'

support_type is confusing pwr and PAL, better use a classiffier or another logic


make it clear:
Thorin

 — 11/11/2025 6:41
Nevermind, I believe I found the solution (Won't delete so people find the solution when searching Discord)

We have to use a Virtual Machine to be able to use our mouse:
https://github.com/Magody/Umaplay/blob/main/docs/README.virtual_machine.md


antonioxxx2

 — 11/11/2025 17:11
estoy viendo que en algunas carreras el mouse queda entremedio de concierto y next

Rosetta — 13/11/2025 13:14
I don't have a log but sometimes when I schedule the Japanese Derby and the recommended race is a random OP one, it'll go for the Japanese Oaks instead - maybe because it's on the first screen and the Derby isn't, but the Satsuki Sho doesn't have this problem


Unknown

 — 15/11/2025 10:14
Weird bug, but the bot buys late surger straightaways when I put pace chaser and pace chaser straightaways on late surger runs
put positive / negative tokens

Rosetta — 15/11/2025 10:16
To fix that go to core\actions\skills.py, edit it in notepad and find the confidence that says 0.75 # experimental and change the 0.75 to 0.9
The only issue I've had since then is firm/wet conditions
But I added that to the skill override json

FreedomArk — 11:00
this is a minor gripe suggestion but is it possible to have a switch where it just stops upon detecting its the crane game? sometimes i leave it in the background on another screen while watching shows and can at least manual the crane game in the off chance it pops up.



important bug thread link: https://discord.com/channels/1100600632659943487/1438783548390641789


### 0.4.3
optimize CNN predicts with ONNX runtime for CPU automatically

Fat Raccoon

 — 14/11/2025 0:30
Is there any way to increase the speed of the bot or is it meant to stay at that speed to prevent issues?

.315 — 14/11/2025 0:09
The bot always use a clock when failing a race even when i set it to stop on failed race
It uses the clock then stop
I think it mistake the "try again" button for the "next" button
Is there a fix for it ?



## 0.5

### 0.5.0

Add R cards

Bat and executable:
- bat is failing
- Executable in release

Team trial
- Prioritize the ones with 'With every win' (gift)

Skill Buying:
- @EO1: List what skills the bot should prioritize and any that isn't in the selection it will randomally get in the list of skills to automatically pick: like if for the 1st part I know I need a certain uma stamina skill to win, then i would 9/10 times get it first. Add auto buy best option based on running style (with a premade priority list)

Bot Strategy / Policy:
- configurable scoring system for rainbows, explosion, combos
"""@EO1:
I also like to add one other idea, maybe like a prioritize support card you want so like kitasan or maybe Tazuna since I am not sure how pals are intergrated in the script

@Undertaker-86 Issue at Github:
Each card also has a different "rainbow bonus". For instance, the Manhattan Cafe STAM card has 1.2 Friendship multiplier, while Super Creek STAM has 1.375, so Super Creek should nudge the bot to click it more than Manhattan Cafe.
"""
- Put parameter in web ui, to decide when is 'weak' turn based on SV or others configs. """Weak turn classifications is used to decide if go to race, rest or recreation instead of training"""
- Change text to: Allow Racing when 'weak turn'
- @EpharGy: Director / Riko Kashimoto custom configs: option to add more and more weight to the Director with the aim to be green by 2nd Skill  increase check.
- Slight WIT nerf on weak turns (prevent over-weighting).
- put rainbow in hint icon or something like that it is not clear what it is right now
- after two failed retried, change style position to front

Team trials:
- handle 'story unlocked'  (press close button), before shop. And "New High score" message (test on monday)
- infinite loop when nothing to do in team trials but in go button check log 'log_team_trials_0.5.0.txt'
- improve team trials the 6 clicks, check if we are in that screen and do as much or as less clicks as needed instead of precomputing

Shop:
- Error loop in shop when nothing to buy, partial state, check on debug 'log_shop_0.5.0.txt'


- transparent may be happening after pressing 'back' in training
- fix data per trainee, (extra training and others, otherwise fit doesn't work)

Template Matching:
- for 'scenario' how does template matching works? is it used? or only text?

- race scheduler improve the patience when no stars found or similar views. Speed up.
- doc the new data augmentation including data steam checker. We need to keep that in sync with traineed, a way to check if there is consistency or if we have more information or less information in particular areas

@Unknown: do you think you could add a feature to add the minimum fans for the unique upgrade or is that already implemented?


Agent Nav: didn't recognized star pieces and bout shoes, retrain nav with more data

- UX: on hint required skills, only bring the selected on 'skills to buy' to have all in sync, instead of the full list. on required skills make sure standard distance cicle or double circle are the same?

- they added new choices for some events of oguri cap, grass wonders, mejiro mcqueens, mejiro ryan, agnes Tachyon, Sakura Bakushin -> automate the event scrapping

Bug:
- false positive, tried to look for this race on july 1:
10:03:03 INFO    agent.py:789: [planned_race] skip_guard=1 after failure desired='Takarazuka Kinen' key=Y3-06-2
10:03:03 INFO    agent.py:241: [planned_race] scheduled skip reset key=Y3-06-2 cooldown=2
10:03:04 DEBUG   lobby.py:796: [date] prev: DateInfo(raw='Senior Year Early Jun', year_code=3, month=6, half=2). Cand: DateInfo(raw='Senior Year Early Jul', year_code=3, month=7, half=1). accepted: DateInfo(raw='Senior Year Early Jul', year_code=3, month=7, half=1)
10:03:04 INFO    lobby.py:797: [date] monotonic: Y3-Jun-2 -> Y3-Jul-1

- for trainee matcher, train a classifier, for now keep template matching. With label studio train the classifier
- 'pre-process' based on the preset, and use the preprocess to speed up the progress


@Rocostre:
"""
test it in JP version to bring plugins and more:
came across this repository a while back while using the Japanese version, and it worked incredibly well — even to this day. I was wondering if you could take a look at the logic behind it and suggest any possible fixes or improvements on your current project. Not sure if this helps or if you're already familiar with it.

https://github.com/NateScarlet/auto-derby


for the pluggins themselves it looks like they are custom macros or logic that other users generated or contribuited for the project to run certain events or training for example there are specific pluggins for an uma training in an specific way to get specific results here is the directory in the repo https://github.com/NateScarlet/auto-derby/wiki/Plugins is all in jap so youll need to translate it.

and here are training results posted by other users that used specific pluggins during training https://github.com/NateScarlet/auto-derby/wiki/Nurturing-result
"""

@Rocostre:
fair enough... also if you can at some point you can add the bot to have an optional setting to auto purchase skills based on currect uma stats to compensate and for the current next race, if possible, for example even if you set up priotity skills to buy but when you are about to purchase skills you don have your desired skills bot will look for alternate skills that are availble that will help you on your next race.
im going to try it out with air grove and see what happens

### 0.5.1
vestovia — Yesterday at 7:37
hi! thank you for the umaplay bot, i understand you avoid emulators due to the inherent risk, but just wondering if adb support or support for other emulators is in the plans? im currently using mumuplayer for the 60fps+ as sometimes i play manually and i think it also might allow it to run in the background like uat? though i think i can use rdp for the meantime but it would be nice. thank you again!

EpharGy — 0:11
Any thoughts on making presets more modular? or giving the ability to use a full preset or a modular one?
ie Character, Race Style, Race Length, Other (CM specific or other skills)?
for example, it's pretty tedious to switch out skills for different Styles and CM's

could then mix and match as needed
Maybe not even make predefined modules, but just have it so you can load multiple preset files and it will basically join them,  could leave it up to the user on what details they add in what presets. May need to de-duplicate or look for clashes, or maybe just prioritize based on load order?

### 0.5.2
support friend bar when overlapped by support_hint, make sure we don't confuse colors or classification
new library, try to handle autoinstall


Etsuke cures slacker


allow buying in unity cup race day, take skill pts some steps before to have something kind of updated?

adb
## 0.6

### 0.6.0

General:
- Connection error handler (“A connection error occurred”): detect dialog with **white** and **green** buttons; handle “Title Screen” and “Retry”.
- classifier transparent or not? handle transparents, only on main parts like screen detector (lobby)? or simple do multiple clicks when selecting  option in lobby to avoid pressing transparent. WAIT in back and after training

Bot Strategy / Policy:
- Better turn number prediction (11 or 1 for example, fails)
- Final Season: consider turn number on strategy and configuration; avoid Rest on last turn but allow earlier.
- optimization formula as recommended in a paper shared on discord
- For fans goals, we can wait a little more,  like winning maiden, we don't need to take it immediattly we can wait for weak turn add  configuration for this

QoL:
- Adapt Triple Tiara, Crown, and Senior preconfigs for race scheduler
- improvement: show data about support cards: which skills they have, and more, also for trainees. Like gametora

Coach (assistant / helper instead of Auto):
- @Rocostre
"""
As I was experimenting with it, I thought it would be great if, in a future update, you could experiment with an AI coach or something similar. This could involve adding an overlay to the game that provides guidance based on the current preset and its own calculations. Instead of relying solely on an automated bot, it could also offer an option for an overlay assistant to suggest actions.
LLM?
"""


Bot Strategy:
- Rest and recreation during Summer Camp now cures bad conditions
- Resting now has a chance to cure the Night owl and skit outbreak
- You can cure slow metabolism by doing some training


check that support bar is intersecting the support box, otherwise sometimes is not inside at all
## 0.7

### 0.7.0

General:
- More human like behavior

Bot Strategy:
- Fast mode: like human pre check rainbow buttons / hints, to decide if keep watching options or not. For example if rainbows in 2  tiles then we need to investigate, otherwise we can do a shortcut
- Fans handling for “director training” decisions or similar events.

End2End navigator play:
- Github Issue





## To validate

@Chat Ja
"""
sorry to dm. my english not good. i found problem on dev branch. could you increase margin top and decrease margin bot ? thank you !
"""

PhantomDice —> Thanks for supporting project


Unity cup:
- Model trained in heavier YOLO model

ADB support:
Thanks for Adding ADB support @C

Automatic scrapping for data
Thanks! @Only

#### General Strategy / Policy:
- Parameter to define 'weak turn':
"""
Author notes: So, when I say weak turns, I mean there are some turns where we usually prefer to skip, and that's why we are using the weak part to skip the turn. And we need to define in the web UI, for both URAfinel and UnityCube, a way to set up which value is considered a weak turn. For example, for UnityCube, it may be by default 1.75, and for URA, it could be 1 in general.
"""
- Speaking of minimum mood, if it's great you often see the bot recreate for the first 2 turns, is it possible to perhaps have a different minimum mood option for the junior year or if energy is full and a friendship can be raised do that instead?
"""
Author notes: We can have also for both scenarios, for all scenarios, a sharded option for a toggle that when clicked, it will show a different mood option that will be triggered only for junior year. So they can set the minimal mood, but that will be only for junior year.
"""
- Lookup toggle: allow skipping **scheduled race** if training has a minimum defined SV like **2.5+ SV if URA or 4 if Unity Cup**. This should be configurable in web ui
  “Check first” at lobby: pre-turn heuristics before going to infirmaty, rest, etc. Pre lookup
  "Check first" allowed for races individually set
"""
Author notes: We’re making a decision to enter the Training phase. Inside Training, we rely on an additional decision layer — essentially another flowchart — to determine what to do during that specific training turn.

This section explains how, in some cases, we might want to check for higher-priority actions before committing to a greedy choice like Training. For instance, going to the Infirmary might be important but not necessarily urgent.

I’d like to introduce a toggle in the Web UI that applies to all scenarios. When this toggle is enabled in a preset, the bot should evaluate some additional conditions before performing its usual greedy actions in the lobby. Usually, we prefer to define such behaviors within presets, as it allows better configurability.

Let’s go through some examples:

1. Infirmary

If the toggle is enabled, before going to the infirmary, we should first check whether the Training screen contains a high-value opportunity.
Specifically, if there’s a super high Support Value (SV) — say, ≥ 3.5 in Unity Cup or ≥ 2.5 in URA — then we should skip the infirmary this turn and train instead, planning to visit the infirmary on the next turn. This logic is straightforward.

2. Auto-Rest Minimum

For the auto-rest rule, however, the toggle doesn’t override anything.
Even if the toggle is active, if the player’s energy is below the auto-rest minimum, the bot should always rest, without any additional checks. This rule must remain absolute.

3. Summer Handling

Similarly, for summer proximity, the existing logic should remain unchanged.
If summer is two or fewer turns away and energy is low, the bot should focus on recovering energy so that it enters summer in good condition — this must be respected even when the toggle is enabled.

4. Goal Races (Critical Goals)

Things get more complex for races, particularly those related to critical goals.
If a mandatory goal race (like a G1, Maven, or fan milestone) is approaching, the bot must still respect the rule for maximum waiting turns before racing.

For example, if the maximum allowed wait time before a goal race is 8 turns, and we’re currently at turn 13, we shouldn’t immediately take the race when we first detect it. Instead, we wait until the number of turns remaining equals 8, or possibly –1 if OCR failed and we couldn’t read it correctly.

If the toggle is enabled, we can make this rule slightly more flexible:

Before racing, check whether there’s a very good Training opportunity.

If there is, we can take that training instead of racing immediately.

However, once the turns left reach ≤ 5, we must proceed to the race, regardless of the toggle.

This ensures the toggle won’t cause failed runs by endlessly delaying goal races just because of attractive training options.

5. Optional / Planned Races

For optional races (those not tied to mandatory goals), the logic differs.
Since these races aren’t required, we should allow users to mark specific planned races as tentative.

At the Web UI level, this would mean adding a per-race toggle in the scheduler.
If this toggle is on for a given race, the bot should, before racing, scan the training screen for good options:

If a valuable training tile is found, the bot should train instead of racing.

If not, it proceeds with the race as usual.

This gives users fine-grained control:

Races marked with the toggle ON are tentative, meaning “only race if no strong training options exist.”

Races with the toggle OFF are mandatory, meaning the bot must race regardless of available training options.

By combining these controls, we gain better configurability, reduce the number of failed or suboptimal runs, and make the decision-making process much more adaptive to each preset and scenario.

Summary:
The new toggle provides a “pre-check” layer before greedy decisions like Infirmary, Rest, or Race actions. It allows the system to momentarily consider higher-value training opportunities but still respects critical safeguards (energy minimums, summer proximity, and goal deadlines). The final behavior should balance flexibility with safety, ensuring the bot neither skips essential actions nor wastes high-value turns.
"""


#### PAL Policy:
- Capture in lobby stats 'Recreation PAL' for later trainig decisions. YOLO model can detect that
"""
Author notes:
In this model, we are capturing a special class just for this RecreationPawl and it's a pink little icon and we should store that in memories so we can use this in next steps. Even more, every time we have a pawl, we need to know in which chain we have this pawl because if this pawl can have 5 dates, 5 chains, and the first chain for example will regenerate some energy, the second one will generate some energy, there will be some special chain step that will not generate that particular energy and we need to keep that in memory and if we know that there is this RecreationPawl icon, we can press the RecreationPawl icon and a pop-up will be displayed and we can just capture the chain steps there. So we know how many chain steps we have and we can take some decisions for this.
"""


- Use dating with pal (if it give energy), as replacement of REST and RECREATION
"""
Author notes: This is literally something, like, I think it's the same as mentioned before, because we either in summer and summer or normal rune we can just have this facility of going to rest or recreation. In case of summer, those options are merged, so anyway. So I think we need to have this option in the web UI. So by default, no, sorry, we don't need this in web UI because this should be a default behavior. If we need energy and we have some events to be triggered from the PAL, we should go back and just take the recreation with the PAL.
"""

- @Rosetta: Tazuna blue was worth more, you want to get it to green ASAP to unlock her dates (there's a bonus if you do it in the junior year)
"""
Author notes: Regarding this requirement, I think I already worked on it. Probably it's done. But let's check that this is implemented in EURA and UnityCup. Basically, I think if the PAL either TASUNA or Super Kashimoto or a support card that contains inside a support PAL icon, this is not very effective. So maybe we want to use this just as a final fallback. But in general, if we have this TASUNA or Kashimoto, we should give more points to if they have the blue color. And I will say if they have blue color, let's add a score of 1.5. I think I already did that anyway. So we can go to green as fast as possible. Maybe we can do that logic for now and we can improve later.
"""

- Some options doesn't give energy, but move the event chain, handle that if 'weak turn'. If we don't know in which chain number we are, open the recreation / collect and go back
"""
Author notes: So, as you can see in the event catalog, some options for Tasuna or Super Kashimoto will not give us energy, will give us stats, so we need to be very careful if we detect a weak turn, but the event chain, let's say we are using a Pal that in its event, in the next event, let's say we are in the second chain right now, after we can collect that information, so let's say we are in the second chain, that means that the next date we will have with the Pal will be the third chain, but let's say for this particular Pal, they will not give us the energy in the third chain, so we need to be careful here because if we need energy and we decide to go back and go using the rest option from this Pal, we will have problems, definitely we will have some problems there because we will not be generating energy, but if we are going back with the reason of do it to, we need recreation, yeah, it doesn't matter if this next chain, this next event will not give us energy, it doesn't matter because we are going back just for the mood increasing or just for the stats, because this is another one, even if we don't need energy or mood increasing, we may detect a weak turn and we should prioritize going with Riko Kashimoto if we have enough energy available to be recovered, so we can move the event chain because our objective is to finalize the date as fast as possible, but only if we have a weak turn and we have some energy to restore, so only if it's worth to do that. Thank you.
"""


- On Weak turn, if energy is not full and recreation is there with a turn that give us energy, use the pal.
"""
Author notes: We are already collecting a weak turn value from YBY, and we should leverage that parameter, or at least make sure we are leveraging properly that. And on weak turn, in weak turn, not a strong turn, sometimes we are deciding in the policy, either in EURA or Unity Cup, we are deciding to go to rest. But if we previously captured that we have this PAL icon, that means that we can have dates, and we can trigger some chain events, and those chain events will be better than going to rest. So, if we have a weak turn, and we know that we need energy, or we need recreation, we can just go back and take the recreation, and take the support PAL recreation.
"""

- @Rosetta: Speaking of Tazuna, I'd like to see an option that when auto rest is supposed to trigger and mood is below minimum, recreation takes priority
"""
Author notes: Again, something similar as before, so we're using this AutoRest, I think the default value is 20%, so if we are triggering the AutoRest option, before just selecting the Rest option, let's check if we have the PAL available, and if we have that, then we should then we should just take the recreation, that would be better, as I told you before, so it's something similar as before, but this is just regarding the lobby policy, I think, that you can review in the policies documentation.
"""

- IF auto rest and more than october in senior year and pal icon, let's go to use that even if mood is not great
#### General UX:
- Advanced settings: changing external processor takes too much time, improved 


#### Unity Cup Policy:
- Prioritize spirit on junior and classic. Reduce its score in Senior
"""
Author notes: This one is very important, because I think we need to increase the value of White Spirit. I think right now we are using 0.4, but if we are in Junior and Classic year, we should increase that by 2. Maybe we can just use 0.8, or well, let's just define a multiplier, we can change that later, but we should give more importance to White Spirit in Classic year and Junior year. In Senior year we should go back to the default values for White Spirit. And we should also give more importance to GPT-4 in Junior year. So, we are going to increase the value of GPT-4 in Junior year, and we are going to increase the value of GPT-4 in Senior year.And the same goes to the White Spirit combo and the Blue Spirit combo. We may want to increase those scores a little with a little multiplier like 1. I think we can define for each one, maybe we can use 1.2 multiplier for the combos or 1.5 maybe is better. And we should disable that if we notice that we are in either final season or in the senior year, in the third year.
"""

- Web UI, selector for first team opponent and the 'rest'
"""
Author notes: So, Unity Cup has some special races, I think they have 5 races, so we should include that in the web UI, a configuration, and in each race you need to select an opponent, I think right now we are selecting always the second opponent, the opponent in the middle, but by default we will have like 5 races I think, or well, for now let's just have 2 options, the first option is what to, well no, let's have an option for each race, so we will have 5 races, and by default in the first race we want to select the middle option, and the rest we want to select the top option, and I think the default one, if we don't know in which race we are, we should select the top option.
"""


- Configurable scoring system for: rainbow combo score, white spirit values (before senior / in senior), white spirit combo score, blue spirit value combo score
"""
Author notes: I have added some values for the combos, but I would like to also let the users configure this, but I don't want to show this directly in the UI. This is only for UnityCup preset. URA doesn't have the Blue Spirits or similar. In the UnityCup preset, we should have a section that says Advanced Settings in the preset where the bot policy is, I think at the end. If the user presses that Advanced Settings, we will open a new model, and inside that model we will have the scores, so they can set up the combo scores. The other ones may be the same.
"""

- Don't explode in overtrained stats (more than our 'stats caps' in our config)
"""
Author notes: If for some reason we already reached the cap level of a particular stat and that stat is allowed and that stat contains the blue spirit let's not explore that there, otherwise we will be wasting a turn, we will be wasting a stat except if we don't have another option but in general we don't want to explore that because the stat is already overtrained
"""

- Allowed / Disallowed stats for spirit burst.
"""
Author notes: So, we have the Spirit Burst, these explosions, that we should call them Spirit Burst. And here is the idea. Those are only triggered when you train with a blue flame, well, where a blue spirit is. So, if you press the blue spirit, you will consume that. And sometimes that blue spirit is in goods or in a particular stat that we don't want to explode, we don't want to press. So, we should put in a web UI an option to enable or disable some stats where we can do the burst.
"""

- prioritize exploding remanent blue explosions in previous 4 turns before Senior November early (we get skill here) ->. In Last two turns (URA finale), just explode wherever they are if we found a burst.
"""
Author notes: So, I noticed that the blue combo sometimes is not being exploded and we end the career, so we should detect from 4 turns before Dec or Nove early. We should check if we have a blue spirit and we should prioritize them, maybe we can multiply the value by 2 if we notice that we are in those dates, because before that event we will get a skill and the skill depends on how much blue spirit have we exploded, so we need to explode as much as possible. And I would say let's check from 4 turns before, but after Nove early, from Nove late, we should not take too much attention to blue spirit, except if we are in the last 2 turns in the UR Finale, in final season, usually final season has 3 turns, and you can check that probably in the goal, or in the turns left, well not in the goal, because in the goal you can see a text that says like Qualifier, another one Semi-Final, and another one Final, so maybe we can use that to understand in which turn are we now that we know we are in the final season. And if we notice that we are in the last 2 turns of the gameplay, we should just explode the blue spirits, it doesn't matter where they are, where they are.
"""


#### QoL:
- @Rosetta:
"""
Speaking of presets, if it's not too hard could we please have a way of sorting them into tabs/groups or at least be able to change the order in which they are on the list? When you have a lot like I do having to keep pressing the arrows while looking through them all is quite the tedious task
"""

Tentative scheduled races:
- If marked as tentative, bot may first check training tiles and if find a good SV will take it and ignore the tentative scheduled race (not tested at all)