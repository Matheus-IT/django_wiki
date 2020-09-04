from django.shortcuts import render

from . import util


def index(request):
	return render(request, "encyclopedia/index.html", {
		"entries_names": util.list_entries()
	})


def entry_page(request, entry_title: str):
	from collections import namedtuple
	import markdown2

	entry_content = util.get_entry(entry_title)

	if entry_content:
		entry_content = markdown2.markdown(entry_content)
		Entry = namedtuple('Entry', 'title content')
		
		return render(request, 'encyclopedia/entry_page.html', {
			'entry': Entry(entry_title, entry_content),
		})
	else:
		return render(request, 'encyclopedia/error_page.html', { 
			'title': f'{entry_title} not found',
			'message': 'The page you\'re looking for, may not exist 🤔'
		})


def random_page(request):
	from random import randint
	
	entries_titles: list(str) = util.list_entries()

	random_index = randint(0, len(entries_titles)-1)
	random_title = entries_titles[random_index]

	return entry_page(request, random_title)


def new_entry(request):
	return render(request, 'encyclopedia/create_new_entry.html')


def confirm_new_entry(request):
	from django.http import HttpResponse

	title: str = request.POST['title']
	content = request.POST['content']

	if title != '' and content != '':
		entries_titles: list(str) = util.list_entries()

		# see if this entry already exists
		for entry_title in entries_titles:
			if title.upper() == entry_title.upper():
				return render(request, 'encyclopedia/error_page.html', {
					'title': f'{title} already exists',
					'message': 'This entry already exists 😐 try to create another one'
				})

		# if it doesn't exist
		util.save_entry(title, content)

		return entry_page(request, title)
	else:
		return render(request, 'encyclopedia/error_page.html', {
			'title': 'Fill all the fields',
			'message': 'Don\'t leave any blank fields 😉 right?'
		})


def edit_entry(request, entry_title: str):
	from collections import namedtuple

	entry_content = util.get_entry(entry_title)

	Entry = namedtuple('Entry', 'title content')

	return render(request, 'encyclopedia/edit_entry.html', {
		'entry': Entry(entry_title, entry_content)
	})


def save_changes_after_edit(request, entry_title: str):
	entry_content = request.POST['content']

	util.save_entry(entry_title, entry_content)

	return entry_page(request, entry_title)


def search(request):
	import re

	entries_titles: list(str) = util.list_entries()
	searched_value: str = request.GET['search_value']

	entries_that_match: list(str) = []

	for entry_title in entries_titles:
		if searched_value.upper() == entry_title.upper():
			return entry_page(request, searched_value)
		elif re.search(searched_value.upper(), entry_title.upper()):
			entries_that_match.append(entry_title)

	if entries_that_match == []:
		return render(request, 'encyclopedia/error_page.html', { 
			'title': f'{entry_title} not found',
			'message': 'Sorry, no results for this entry 😅'
		})

	return render(request, 'encyclopedia/search_results.html', { 
		'entries_titles': entries_that_match
	})
