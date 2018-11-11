# SPDX-License-Identifier: GPL-2.0-or-later
import argparse
import json
import sys
import xml.etree.ElementTree as ET


parser = argparse.ArgumentParser()
parser.add_argument("filename")


def main():
    args = parser.parse_args()
    tree = ET.parse(args.filename).getroot()
    pages = parse_fotobook_tree(tree)
    print(json.dumps(pages, default=lambda o: o.asdict(), indent=2))


def parse_fotobook_tree(tree):
    assert tree.tag == "fotobook"
    page_trees = [e for e in tree if e.tag == "page"]
    pages = []
    for page_i, page_tree in enumerate(page_trees):
        bundlesize_tree, = [e for e in page_tree if e.tag == "bundlesize"]
        page_height = int(bundlesize_tree.get("height"))
        page_width = int(bundlesize_tree.get("width"))
        area_trees = [e for e in page_tree if e.tag == "area"]
        # TODO: Parse backgrounds
        background_trees = [e for e in page_tree if e.tag == "background"]
        images = []
        for area_i, area_tree in enumerate(area_trees):
            if area_tree.get("areatype") == "spinelogoarea":
                # TODO: This area only has a border.
                continue
            height = float(area_tree.get("height"))
            width = float(area_tree.get("width"))
            top = float(area_tree.get("top"))
            left = float(area_tree.get("left"))
            rotation = float(area_tree.get("rotation"))
            border_trees = []
            try:
                border_tree, content_tree = area_tree
            except ValueError:
                print(
                    "Parse error at page[%s].area[%s]: len(area_tree) == %s"
                    % (page_i, area_i, len(area_tree)),
                    file=sys.stderr,
                )
                continue
            if content_tree.tag == "text":
                # TODO
                continue
            if content_tree.tag != "image":
                print(
                    "Parse error at page[%s].area[%s]: Unknown content tag %s"
                    % (page_i, area_i, content_tree.tag),
                    file=sys.stderr,
                )
                continue
            try:
                relationships_tree, = content_tree
            except ValueError:
                print(
                    "Parse error at page[%s].area[%s]: len(content_tree) == %s"
                    % (page_i, area_i, len(content_tree)),
                    file=sys.stderr,
                )
                continue
            assert relationships_tree.tag == "relationships"
            try:
                relationship_tree, = [
                    e for e in relationships_tree if e.get("parent").startswith("/")
                ]
            except ValueError:
                print(
                    "Parse error at page[%s].area[%s]: len(relationships_tree) == %s"
                    % (page_i, area_i, len(relationships_tree)),
                    file=sys.stderr,
                )
                continue
            assert relationship_tree.tag == "relationship"
            path = relationship_tree.get("parent")
            crop_top = int(content_tree.get("top"))
            crop_left = int(content_tree.get("left"))
            scale = float(content_tree.get("scale"))
            # Image is first cropped, then scaled.
            images.append(
                dict(
                    width=width,
                    height=height,
                    top=top,
                    left=left,
                    crop_top=crop_top,
                    crop_left=crop_left,
                    scale=scale,
                    rotation=rotation,
                    path=path,
                )
            )
        # if not images:
        #     print("Warning at page[%s]: No images" % page_i, file=sys.stderr)
        pages.append(
            dict(page_width=page_width, page_height=page_height, images=images)
        )
    return pages


if __name__ == "__main__":
    main()
