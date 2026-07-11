# Plain-language summary for Kirill

Alchemy is the right next operation to design. The simulator can already add modifiers one at a time and can run fixed sequences. Alchemy is the next useful step because it packages several accepted add decisions into one atomic action: make a Rare item containing four new random modifiers.

The important source correction is now clear. Current official patch notes say Alchemy can be used on Normal or Magic items and that a Magic item's original modifiers are not retained. Current PoE2DB wording says the result is Rare with four random modifiers. That supports the repository's broad "empty Rare working copy, then generate four modifiers" contour.

One important edge is not clear enough to implement silently. Fractured modifiers are normally immutable, while Alchemy replaces original Magic modifiers. Public sources checked do not state what happens when those rules meet. The safest M44-A boundary is therefore non-fractured Normal/Magic equipment only; fractured input must fail unchanged until Kirill/ChatGPT accepts a separately verified rule.

The exact internal distribution of the four-modifier roll is also not public server truth. Reusing the accepted weighted ordinary-add pool four times, rebuilding legality after each selection, is the leanest auditable project-model implementation. It should be accepted explicitly at the M44-A gate, not presented as verified server behavior.
