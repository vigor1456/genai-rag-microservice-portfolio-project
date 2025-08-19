#!/usr/bin/env python
import argparse, json
from app.chain import RAGService

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paths", nargs="+", required=True)
    ap.add_argument("--no-recursive", action="store_true")
    args = ap.parse_args()

    svc = RAGService()
    count = svc.ingest(args.paths, recursive=not args.no_recursive)
    print(json.dumps({"ingested": count}))

if __name__ == "__main__":
    main()
