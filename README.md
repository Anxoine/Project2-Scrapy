# Project 2 Submission

This repository contains fixes implemented for Scrapy issues as part of the course project.

## Branch
All current work is combined in the `final-submission` branch.

## Issues Fixed (Current Progress)

- #1615: FilesPipeline now correctly accepts valid 2xx HTTP responses instead of only 200
- #1163: FormRequest now raises a ValueError when formname or formid does not match any form
- #7010: scrapy settings --get does not account for add-ons
- #6047: Improved unhandled exception handling for Crawler*.crawl()

## Notes
All fixes were implemented following Scrapy's code structure and existing test patterns.

Additional issues and fixes will be added to this branch as the project progresses.
