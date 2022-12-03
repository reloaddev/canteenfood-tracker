// Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
const { executeWriteSql } = require('./utils')

const types = [
  'WEAPON',
  'ARMOR',
  'CLOTHING',
  'POTION'
]

const addItemToUser = async (username) => {
  const itemType = types[Math.floor(Math.random()*types.length)]
  let properties
  if (itemType == 'WEAPON') {
    properties = { attack: Math.floor(Math.random() * 10) + 1  }
  } else if (itemType == 'ARMOR') {
    properties = { defense: Math.floor(Math.random() * 10) + 1  }
  } else if (itemType == 'CLOTHING') {
    properties = { charisma: Math.floor(Math.random() * 10) + 1  }
  } else if (itemType == 'POTION') {
    properties = { healing: Math.floor(Math.random() * 10) + 1  }
  }
  writeSql = `INSERT INTO items (item_id, owner_id, type, properties) \
VALUES (DEFAULT, (SELECT user_id from users where username = :username), :type, :properties) \
RETURNING item_id, owner_id, type, properties`
  writeParameters = [
    {
      name: 'username',
      value: { stringValue: username }
    },
    {
      name: 'type',
      value: { stringValue: itemType}
    },
    {
      name: 'properties',
      value: { stringValue: JSON.stringify(properties)}
    }

  ]
  const writeResult = await executeWriteSql(writeSql, writeParameters)
  return writeResult[0]
}

module.exports = addItemToUser
