from app.api.schemas.auth import MenuNodeDto
from app.domain.entities.menu_item import MenuItem


def build_menu_tree(items: list[MenuItem]) -> list[MenuNodeDto]:
    nodes = {
        m.id: MenuNodeDto(
            id=m.id,
            path=m.path,
            label=m.label,
            icon=m.icon,
            sort_order=m.sort_order,
            children=[],
        )
        for m in items
    }
    roots: list[MenuNodeDto] = []
    for m in items:
        node = nodes[m.id]
        if m.parent_id is not None and m.parent_id in nodes:
            nodes[m.parent_id].children.append(node)
        else:
            roots.append(node)
    roots.sort(key=lambda x: (x.sort_order, x.id))
    for n in nodes.values():
        n.children.sort(key=lambda x: (x.sort_order, x.id))
    return roots
