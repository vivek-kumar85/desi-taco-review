/* Review draft writer for The Desi Taco Co.
   Builds a short draft ONLY from what the customer picked: what they had,
   what they liked and what could be better. It invents no facts (no
   companions, no names, no visit counts). There is no star rating here (the
   customer gives their stars once, on Google), so the tone follows the picks:
   only good things make a happy review, "could be better" picks make it
   balanced, and the food is never called good or bad unless they said so.
   Every draft is mixed at random from large phrase banks, sentence orders,
   punctuation and sign-offs, so two people rarely get the same text; the page
   also remembers recent drafts on each phone and never shows one twice. */
(function (root) {
  function pick(a, rnd) { return a[Math.floor(rnd() * a.length)]; }
  function shuffle(a, rnd) {
    a = a.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(rnd() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function list(x, rnd) {
    if (x.length === 1) return x[0];
    var and = rnd && rnd() < 0.12 ? " & " : " and ";
    return x.slice(0, -1).join(", ") + and + x[x.length - 1];
  }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

  var DISH = {
    "Ghee roast taco": "ghee roast taco",
    "Andhra pepper fry taco": "Andhra pepper fry taco",
    "Punjabi bhuna taco": "Punjabi bhuna taco",
    "Cheese shell taco": "cheese shell taco",
    "Chimichanga": "chimichanga",
    "Kheema thecha quesadilla": "kheema thecha quesadilla",
    "Burrito roll": "burrito roll",
    "Nachos": "nachos",
    "Til gud poli": "til gud poli"
  };
  var PLURAL = { "nachos": true };

  // every highlight is a full clause, so any mix of them lists cleanly
  var GOOD = {
    "Taste": ["the flavours were spot on", "everything was full of flavour", "every bite had proper desi taste", "the food was really tasty", "the masalas were perfectly done"],
    "Spice level": ["the spice level was just right for me", "I loved the kick of spice", "the spice was nicely balanced", "the heat was perfect", "the spice hit the right note"],
    "Big portions": ["the portions were generous", "one plate filled me up", "the portions were really filling", "you get a lot for one order", "I left properly full"],
    "Value for money": ["it's great value for money", "the prices are very fair", "it's really pocket-friendly", "it doesn't burn a hole in your pocket", "the pricing is reasonable"],
    "Quick service": ["the food came out quickly", "the service was quick", "I didn't have to wait long", "the order was ready fast", "they were quick with the order"],
    "Friendly staff": ["the staff were super friendly", "the people at the counter were really friendly", "the team was warm and welcoming", "everyone was polite and helpful", "the staff made me feel welcome"],
    "Veg options": ["there are good veg options too", "vegetarians have plenty to choose from", "the veg options are solid", "the veg fillings are just as good", "it's great for vegetarians too"],
    "The vibe": ["the evening vibe's chill", "the vibe is fun and relaxed", "it's got a nice easy-going vibe", "the place has a fun vibe", "it's a nice chill spot to hang out"]
  };

  var BAD = {
    "Waiting time": ["the wait was a bit long", "I had to wait longer than expected", "the order took a while", "it took quite long to get the food", "the service was slow"],
    "Too spicy": ["it was a bit too spicy for me", "the spice was too much for me", "it was too hot for my taste", "the masala was too strong for me", "it was way too spicy"],
    "Not spicy enough": ["it could have used more spice", "I wanted a bit more heat", "it was a bit mild for me", "I'd have liked it spicier", "it needed more masala"],
    "Small portions": ["portions could be bigger", "the portion felt small", "I was still a bit hungry after", "the quantity was less", "it wasn't very filling"],
    "Price": ["it felt a little pricey", "it's a bit expensive for the size", "prices could be a little lower", "it felt overpriced", "the prices are on the higher side"],
    "Seating": ["seating is limited", "there wasn't much space to sit", "it gets crowded with few seats", "it was hard to find a place to sit", "there's very little seating"],
    "Parking": ["parking was tricky", "finding parking took a while", "parking nearby is hard to find", "there's no easy parking", "parking is a headache"]
  };

  // {d} dish list, {it} it/they, {was} was/were, {is} is/are, {a} adjective
  var TONE = {
    love: {
      open: ["Loved this place!", "What a find in Salunkhe Vihar.", "So glad I tried The Desi Taco Co.", "I'm hooked on this place.", "Desi Taco Co. didn't disappoint.", "This place is a gem.", "Absolutely loved it.", "Such a good find.", "Really happy with this one.", "Can't stop thinking about these tacos.", "So glad I stopped by.", "This spot is a must in Salunkhe Vihar.", "Great desi tacos in Salunkhe Vihar.", "Loved the desi-style tacos here.", "Really good Indian-Mexican food near NIBM.", "Such a fun taco spot in Kondhwa."],
      adj: ["amazing", "so good", "really tasty", "full of flavour", "delicious", "super tasty", "fantastic", "lip-smacking"],
      dish: ["I had the {d} and {it} {was} {a}.", "The {d} {was} {a}.", "I tried the {d}, {a}!", "You've got to try the {d}.", "Ordered the {d} and {it} {was} {a}.", "Big fan of the {d}.", "The {d} {was} the star for me.", "The {d} {is} a must-try."],
      extra: ["Desi flavours in a taco just work.", "Such a nice change from the usual fast food.", "Lots on the menu to try.", "Great spot for an evening snack.", "The fusion is done really well.", "Proper street-food vibes.", "Nothing else like it around here.", "Fresh and full of masala.", "Proper desi tacos with real Indian flavours.", "Mexican food with a proper Indian twist.", "The Indian-Mexican fusion really works.", "Tacos, quesadillas and burritos, all with a desi twist."],
      close: ["I'll definitely be back!", "Must try if you're around NIBM.", "Highly recommend it.", "Can't wait to try more of the menu.", "I'm coming back for more.", "Go try it!", "Totally recommend.", "Already want to go back.", "Will be back soon.", "Recommended for anyone who loves tacos.", "A must for taco lovers in Pune.", "Must try if you're near Kondhwa."],
      emoji: ["🌮", "😋", "🙌", "❤️", "👌"]
    },
    like: {
      open: ["Good experience overall.", "Nice spot for desi-style tacos.", "I enjoyed my visit.", "Pretty good food here.", "A good find in Salunkhe Vihar.", "Liked it quite a bit.", "Solid place for a quick bite.", "Good little place.", "Nice taco place near NIBM.", "Good Indian-Mexican food in Salunkhe Vihar."],
      adj: ["good", "tasty", "nice", "pretty good", "enjoyable", "quite tasty", "really nice"],
      dish: ["The {d} {was} {a}.", "I had the {d}, {it} {was} {a}.", "I tried the {d} and {it} {was} {a}.", "Ordered the {d}, {it} {was} {a}.", "Liked the {d}.", "The {d} {is} worth trying."],
      extra: ["Nice twist on regular tacos.", "Good spot for an evening snack.", "Interesting fusion menu.", "Decent variety on the menu.", "A different kind of taco place.", "Good Mexican food with an Indian twist.", "Nice option for desi tacos in Pune."],
      close: ["I'd come again.", "Worth a try.", "Good option for a quick bite.", "I'll be back to try more.", "Would recommend.", "Will visit again.", "Happy to come back.", "Worth a try for taco lovers."],
      emoji: ["🌮", "👍"]
    },
    mixed: {
      open: ["Decent experience overall.", "Some things were good, some not so much.", "It was a mixed visit for me.", "Okay visit overall.", "Average experience this time.", "Not bad, not great."],
      adj: ["okay", "alright", "decent", "average"],
      dish: ["The {d} {was} {a}.", "I had the {d}, {it} {was} {a}.", "The {d} {was} {a}, nothing special.", "Tried the {d}, {it} {was} {a}."],
      extra: ["The idea is interesting.", "Nice concept.", "The menu has some good ideas.", "Interesting idea, desi flavours in tacos."],
      close: ["I might give it another try.", "Hope it's better next time.", "It could be great with a few fixes.", "Might come back to try something else.", "Has potential."],
      emoji: []
    }
  };

  // words too common to count as a repeat ("the" twice is fine, "spot" twice is not)
  var COMMON = { "the": 1, "and": 1, "was": 1, "were": 1, "for": 1, "with": 1, "this": 1, "that": 1, "it's": 1, "really": 1, "very": 1, "have": 1, "had": 1, "but": 1, "you": 1, "too": 1, "just": 1, "taco": 1, "tacos": 1, "more": 1, "bit": 1, "time": 1, "here": 1, "place": 1, "they": 1, "what": 1, "from": 1, "like": 1, "will": 1 };
  function repeats(text, ignore) {
    var seen = {}, words = text.toLowerCase().match(/[a-z']+/g) || [];
    for (var i = 0; i < words.length; i++) {
      var w = words[i];
      if (w.length < 4 || COMMON[w] || (ignore && ignore[w])) continue;
      if (w.length > 4) w = w.replace(/s$/, ""); // "masala" and "masalas" count as the same word
      if (seen[w]) return true;
      seen[w] = 1;
    }
    return false;
  }

  // Search-friendly, the natural way: Google reads what reviews mention, so a
  // draft should name what people search for (tacos, the dish, the area) once,
  // never stuffed. At most one place name per review, and no "best X in Pune".
  var FOOD_WORD = /taco|quesadilla|chimichanga|burrito|nachos|til gud|fusion|mexican/i;
  var PLACE = /salunkhe vihar|nibm|kondhwa|wanowrie|pune/gi;
  var FOOD_LINE = {
    love: ["Desi flavours in a taco just work.", "Proper desi tacos with real Indian flavours.", "Mexican food with a proper Indian twist."],
    like: ["Nice twist on regular tacos.", "Good Mexican food with an Indian twist."],
    mixed: ["Interesting idea, desi flavours in tacos."]
  };
  function places(text) { return (text.match(PLACE) || []).length; }

  // What the customer typed in an "Other" box: kept in their own words, only
  // tidied (no links, emails or phone numbers, no trailing punctuation, max 60).
  function clean(x) {
    if (!x) return "";
    x = String(x);
    // links, emails and phone numbers don't belong in a review: ignore the whole box
    if (/https?:\/\/|www\.|\S+@\S+\.\S+|\+?\d[\d\s-]{6,}\d/i.test(x)) return "";
    x = x
      .replace(/[<>{}\[\]]/g, "")
      .replace(/\s+/g, " ")
      .trim()
      .replace(/[.,;:!?\s]+$/, "");
    if (x.length > 60) x = x.slice(0, 60).replace(/\s+\S*$/, "");
    return x;
  }
  // "music was great" is already a sentence; "green chutney" is just a thing
  function isSentence(x) {
    return x.split(" ").length >= 2 && /\b(was|were|is|are|had|have|loved|liked|could|should|felt|tasted)\b/i.test(x);
  }
  function asSentence(x) { return cap(x) + "."; }
  function thing(x) { return /^[A-Z]/.test(x) ? x : "the " + x.replace(/^the\s+/i, ""); }
  function plural(x) { return /[^s]s$/i.test(x); }
  function customLiked(x, rnd) {
    if (isSentence(x)) return asSentence(x);
    var t = thing(x);
    return pick(/^[A-Z]/.test(x)
      ? ["Big shoutout to {t}!", "Special mention for {t}."]
      : ["Also loved {t}.", "Special mention for {t}.", cap("{t} " + (plural(x) ? "were" : "was") + " a nice touch.")], rnd).replace("{t}", t).replace(/^the/, "The");
  }
  function customBetter(x, rnd, soft) {
    if (isSentence(x)) return asSentence(x);
    // a request in their own words ("more sauce please") stays as they wrote it
    if (/^(more|less|add|extra|bigger|smaller|faster|cheaper|some|please)\b|\bplease\b/i.test(x)) return (soft ? pick(["Only thing: ", "One small request: "], rnd) + x : cap(x)) + ".";
    var t = thing(x);
    var line = pick(soft
      ? ["Only thing, {t} could be better.", "One small thing: {t} could be improved."]
      : ["{T} could be better.", "{T} needs work.", "Would like {t} to improve."], rnd);
    return line.replace("{T}", cap(t)).replace("{t}", t);
  }

  // Tone from the picks, never from a rating: nothing to improve reads happy
  // (mostly very happy), one thing to improve reads happy with a small note,
  // and more complaints than likes reads balanced.
  function toneOf(choice, rnd) {
    var liked = (choice.liked || []).filter(function (k) { return GOOD[k]; }).length + (clean(choice.otherLiked) ? 1 : 0);
    var better = (choice.better || []).filter(function (k) { return BAD[k]; }).length + (clean(choice.otherBetter) ? 1 : 0);
    if (!better) return rnd() < 0.7 ? "love" : "like";
    if (better === 1) return liked >= 2 && rnd() < 0.5 ? "love" : "like";
    return liked >= better ? "like" : "mixed";
  }
  // a plain mention of the dish, for when we can't tell how the food itself was
  var PLAIN_DISH = ["I had the {d}.", "Tried the {d}.", "Ordered the {d}.", "Went for the {d}.", "Had the {d} this time."];

  function clauses(keys, bank, rnd, max) {
    var out = [];
    shuffle(keys, rnd).slice(0, max).forEach(function (k) { if (bank[k]) out.push(pick(bank[k], rnd)); });
    return out;
  }

  function once(choice, rnd) {
    var tier = toneOf(choice, rnd), T = TONE[tier];
    var dishes = (choice.had || []).filter(function (h) { return DISH[h]; }).map(function (h) { return DISH[h]; });
    var otherHad = clean(choice.otherHad), otherLiked = clean(choice.otherLiked), otherBetter = clean(choice.otherBetter);
    if (otherHad) dishes.push(otherHad);
    var good = clauses(choice.liked || [], GOOD, rnd, 3);
    var bad = clauses(choice.better || [], BAD, rnd, 2);
    var soft = tier === "love" || tier === "like";
    var likedLine = otherLiked ? customLiked(otherLiked, rnd) : "";
    var betterLine = otherBetter ? customBetter(otherBetter, rnd, soft && !bad.length) : "";

    var goodLine = good.length ? cap(list(good, rnd)) + "." : "";
    // no verdict on the food when the review is balanced or their own words
    // could be about the food ("taste was bland" next to "it was tasty")
    var plain = tier === "mixed" || !!otherBetter;
    var dishLine = "";
    if (dishes.length) {
      var ds = shuffle(dishes, rnd).slice(0, 3);
      if (otherHad && ds.indexOf(otherHad) < 0) ds[ds.length - 1] = otherHad; // never drop what they typed
      var many = ds.length > 1 || PLURAL[ds[0]] || (ds[0] === otherHad && plural(otherHad));
      dishLine = pick(plain ? PLAIN_DISH : T.dish, rnd)
        .replace("{d}", list(ds, rnd))
        .replace("{it}", many ? "they" : "it")
        .replace("{was}", many ? "were" : "was")
        .replace("{is}", many ? "are" : "is")
        .replace("{a}", pick(T.adj, rnd));
    } else if (!plain && rnd() < 0.8) {
      // no dish picked: a general line about the food, in the review's tone
      dishLine = pick(["Everything I tried was {a}.", "The food was {a}.", "All of it was {a}.", "What I ordered was {a}."], rnd)
        .replace("{a}", pick(T.adj, rnd));
    }
    var badLine = "";
    if (bad.length) {
      badLine = (tier === "love" || tier === "like")
        ? pick(["Only thing, ", "One small thing: ", "If anything, ", "Just one thing, "], rnd) + list(bad, rnd) + "."
        : cap(list(bad, rnd)) + ".";
    }
    var extra = T.extra.length && rnd() < (tier === "love" || tier === "like" ? 0.4 : 0.3) ? pick(T.extra, rnd) : "";

    var middle = [];
    if (tier === "love" || tier === "like") {
      middle = shuffle([dishLine, goodLine, likedLine, extra].filter(Boolean), rnd);
      if (badLine) middle.push(badLine);
      if (betterLine) middle.push(betterLine);
    } else {
      [dishLine, badLine, betterLine].forEach(function (s) { if (s) middle.push(s); });
      if (goodLine) middle.push(pick(["On the plus side, ", "That said, ", "Good part: "], rnd) + goodLine.charAt(0).toLowerCase() + goodLine.slice(1));
      if (likedLine) middle.push(likedLine);
      if (extra) middle.push(extra);
    }

    var parts = [];
    var lead = rnd() < (tier === "love" ? 0.7 : 0.8);
    if (lead || middle.length < 2) parts.push(pick(T.open, rnd));
    parts = parts.concat(middle);
    if (parts.length < 3 || rnd() < 0.75) parts.push(pick(T.close, rnd));
    // make sure the review says what the place serves at least once
    if (!FOOD_WORD.test(parts.join(" "))) {
      var at = parts.length > 1 ? 1 + Math.floor(rnd() * (parts.length - 1)) : parts.length;
      parts.splice(at, 0, pick(FOOD_LINE[tier], rnd));
    }

    // a few exclamation marks on happy reviews, the way people actually type
    if (tier === "love" || tier === "like") {
      var bangs = 0, maxBangs = tier === "love" ? 2 : 1;
      parts = parts.map(function (s) {
        if (/!$/.test(s)) { bangs++; return s; }
        if (bangs < maxBangs && /\.$/.test(s) && rnd() < 0.22) { bangs++; return s.slice(0, -1) + "!"; }
        return s;
      });
    }

    var text = parts.join(" ");
    if (T.emoji.length && rnd() < (tier === "love" ? 0.35 : 0.2)) text += " " + pick(T.emoji, rnd);
    return text;
  }

  function draft(choice, rnd) {
    rnd = rnd || Math.random;
    // the customer's own typed words may repeat; only our wording must not
    var ignore = {};
    [choice.otherHad, choice.otherLiked, choice.otherBetter].forEach(function (x) {
      (clean(x).toLowerCase().match(/[a-z']+/g) || []).forEach(function (w) { ignore[w] = 1; ignore[w.replace(/s$/, "")] = 1; });
    });
    var text = once(choice, rnd);
    for (var i = 0; i < 40 && (repeats(text, ignore) || places(text) > 1); i++) text = once(choice, rnd);
    return text;
  }

  var api = { draft: draft, DISH: DISH, GOOD: GOOD, BAD: BAD, repeats: repeats, places: places, FOOD_WORD: FOOD_WORD };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.ReviewDraft = api;
})(this);
