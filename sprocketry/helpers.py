

def get_word_feature(w, feature):
    if not hasattr(w, "features"):
        w.features = dict(pair.split("=") for pair in w.feats.split("|")) if w.feats is not None else dict()
    return w.features[feature] if feature in w.features else None


def word_is_finite_verb(w):
    return get_word_feature(w, "VerbForm") == "Fin"


def word_is_verb(w):
    verb_form = get_word_feature(w, "VerbForm")
    return verb_form is not None