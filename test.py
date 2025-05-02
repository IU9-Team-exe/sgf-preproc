import sgfmill.sgf

sgf_file = 'test/pro_1.sgf'
with open(sgf_file, "r", encoding="utf-8") as f:
    sgf_content = f.read()

game = sgfmill.sgf.Sgf_game.from_string(sgf_content)
nodes = [i for i in game.main_sequence_iter()]
# print(nodes[2])
for i, j in enumerate(nodes):
    # print(f"{i} node: {j}")
    if j.has_property("C"):
        comment = j.get("C")
        print(f"Move {i}: {comment}, type={type(comment)}")
